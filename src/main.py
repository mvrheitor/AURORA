from src.config import *

def carregar_prompt():
    with open("src/prompt.txt", "r", encoding="utf-8") as f:
        return f.read()

def enviar_msg(client, mensagens):
    resposta = client.chat.completions.create(
        messages=mensagens,
        model="openai/gpt-oss-120b",
        max_completion_tokens=1000,
        temperature=0
    )
    
    mensagens.append({
        'role': 'assistant',
        'content': resposta.choices[0].message.content
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
        resposta = enviar_msg(client, mensagens)

        print("\n=== RESPOSTA:")
        print(resposta.choices[0].message.content)
