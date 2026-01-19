from src.config import *
from src.tools.schemas import tools
from src.tools.registry import funcoes_disponiveis
import json

import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import threading

samplerate = 44100
arquivo_saida = "./temp/temp.wav"

def gravar():
    #Função que coleta áudio em frames enquanto 'gravando' é True
    global frames, gravando
    frames = []
    with sd.InputStream(samplerate=samplerate, channels=1, dtype="int16") as stream:
        while gravando:
            data, _ = stream.read(1024)
            frames.append(data.copy())

def carregar_prompt():
    with open("src/prompt.txt", "r", encoding="utf-8") as f:
        return f.read()

def enviar_msg(client, mensagens, tools):
    resposta = client.chat.completions.create(
        messages=mensagens,
        model="openai/gpt-oss-120b",
        max_completion_tokens=1000,
        temperature=0,
        tools=tools,
        tool_choice="auto"
    )

    print("\n=== PENSAMENTO: ")
    print(resposta.choices[0].message.reasoning) # mostra o pensamento da Aurora

    tool_calls = resposta.choices[0].message.tool_calls

    if tool_calls:
        print("\n=== TOOL CHAMADA:")
        for i in tool_calls:
            print(f"- {i.function.name} --> {i.function.arguments}") # mostra a função chamada, bem como os argumentos

        mensagens.append(resposta.choices[0].message)

        for tool_call in tool_calls:
            function_to_call = funcoes_disponiveis[tool_call.function.name]
            function_args = json.loads(tool_call.function.arguments)

            if function_args:
                function_response = function_to_call(**function_args)
            else:
                function_response = function_to_call()

            mensagens.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": tool_call.function.name,
                "content": function_response,
            })

        return enviar_msg(client, mensagens, tools)

    mensagens.append({
        "role": "assistant",
        "content": resposta.choices[0].message.content
    })
    return resposta

def iniciar_chat():
    client = get_client()
    
    mensagens = [{
        'role': 'system',
        'content': carregar_prompt()
    }]

    os.system("clear")

    print("\nAurora iniciada. Digite 'sair' para encerrar.")

    while True:
        prompt = input("\nPressione Enter para falar.")

        gravando = True
        thread = threading.Thread(target=gravar)
        thread.start()

        input("Ouvindo...")
        gravando = False
        thread.join()

        # Concatena frames e salva em arquivo
        audio = np.concatenate(frames, axis=0)
        write(arquivo_saida, samplerate, audio)

        with open(arquivo_saida, "rb") as f:
            transcricao = client.audio.transcriptions.create(
                model="whisper-large-v3",
                file=f,
                language='pt'
            )
        
        prompt = transcricao.text
        print("Transcrição:", prompt)

        mensagens.append({'role': 'user', 'content': prompt})
        resposta = enviar_msg(client, mensagens, tools)

        print("\n=== RESPOSTA:")
        print(resposta.choices[0].message.content)
