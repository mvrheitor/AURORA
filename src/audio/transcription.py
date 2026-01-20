def transcrever_audio(client, arquivo, language="pt"):
    with open(arquivo, "rb") as f:
        transcricao = client.audio.transcriptions.create(
            model="whisper-large-v3",
            file=f,
            language=language
        )
    return transcricao.text
