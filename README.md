# AURORA v3.0.1
Autonomous Utility for Reasoning, Operations & Rapid Assistance

AURORA é um assistente inteligente inspirado em sistemas como o Jarvis, capaz não apenas de conversar, mas também de executar ações reais no sistema operacional através de ferramentas (tools).

A partir da versão 3.0.0, a Aurora suporta reconhecimento de voz, permitindo interação por áudio.

---

## ⚠ Avisos importantes

- Este projeto executa comandos reais no sistema operacional.  
  Use apenas em ambientes controlados e por sua conta e risco.

- As tools foram desenvolvidas exclusivamente para sistemas Linux.  
  O funcionamento em Windows ou macOS não é garantido e exigirá adaptações no código.

---

## Principais funcionalidades

- Chat interativo via terminal
- Reconhecimento de voz com captura de áudio pelo microfone e transcrição com IA
- Execução de comandos reais no sistema operacional
- Sistema de tools integrado à LLM
- Loop que permite que AURORA decida executar múltiplas tools em sequência
- Exibição do pensamento da AURORA
- Exibição das tools chamadas e seus argumentos
- Prompt configurável externamente
- Estrutura modular de projeto (src, tools, schemas, registry)

---

## Instalação

```
git clone https://github.com/mvrheitor/AURORA.git
cd AURORA
pip install -r requirements.txt
cp .env.example .env
```
Coloque sua chave da Groq no .env.

## Uso
```
python run.py
```

> [!tip] Dica
> Para uma melhor experiência, altere informações como nome e sistema operacional no prompt.

## Requisitos:
- Microfone funcional
- PortAudio instalado no sistema
- API da Groq (grátis)