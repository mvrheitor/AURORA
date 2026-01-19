from src.config import *
from src.tools.schemas import tools
from src.tools.registry import funcoes_disponiveis
import json

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

    tool_calls = resposta.choices[0].message.tool_calls

    if tool_calls:
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
        prompt = input("\nDigite sua mensagem: ")

        if prompt.lower() == "sair":
            print("Encerrando Aurora...")
            break

        mensagens.append({'role': 'user', 'content': prompt})
        resposta = enviar_msg(client, mensagens, tools)

        print("\n=== RESPOSTA:")
        print(resposta.choices[0].message.content)
