from src.config import *
from src.tools.schemas import tools
from src.tools.registry import funcoes_disponiveis
from src.audio.recorder import Gravador
from src.audio.transcription import transcrever_audio
from scipy.io.wavfile import write
from pathlib import Path
import json
import os

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

    gravador = Gravador()
    samplerate = 44100
    
    BASE_DIR = Path(__file__).resolve().parent
    TEMP_DIR = BASE_DIR / "audio"
    TEMP_DIR.mkdir(exist_ok=True)

    arquivo_saida = TEMP_DIR / "temp.wav"

    mensagens = [{
        'role': 'system',
        'content': carregar_prompt()
    }]

    os.system("clear")

    print("\nAurora iniciada. Digite 'sair' para encerrar.")

    while True:
        prompt = input("\nPressione Enter para falar.")
        
        gravador.iniciar()

        input("Ouvindo... pressione Enter para parar.")
        audio = gravador.parar()

        write(arquivo_saida, samplerate, audio)

        prompt = transcrever_audio(client, arquivo_saida)
        print("Transcrição:", prompt)

        mensagens.append({'role': 'user', 'content': prompt})
        resposta = enviar_msg(client, mensagens, tools)

        print("\n=== RESPOSTA:")
        print(resposta.choices[0].message.content)
