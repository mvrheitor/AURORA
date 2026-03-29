import subprocess
import threading
import time

# Usamos um marcador para saber quando o terminal terminou de processar um comando
MARKER = "__AURORA_CMD_DONE__"

class TerminalSession:
    def __init__(self, shell="/bin/bash"):
        # 1. Iniciamos o terminal real
        # text=True já cuida da decodificação de bytes para strings (utf-8)
        # stderr=subprocess.STDOUT junta os erros com a saída normal (mais fácil pra IA ler)
        # bufsize=1 garante que a saída seja liberada mais rápido
        self.process = subprocess.Popen(
            [shell],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        self.buffer = ""
        self.status = "free"  # Estados possíveis: 'free', 'busy', 'waiting_input'

        # 2. Iniciamos o "Ouvinte" em segundo plano
        # Essa Thread fica lendo o terminal sem travar o seu código principal
        self.reader_thread = threading.Thread(target=self._ouvir_terminal, daemon=True)
        self.reader_thread.start()

    def _ouvir_terminal(self):
        """Fica lendo a saída do terminal caractere por caractere."""
        while True:
            # Ler 1 caractere por vez é o segredo para não travar em comandos de 'input()'
            char = self.process.stdout.read(1)
            if not char:
                break  # O terminal foi fechado
            self.buffer += char

    def send_command(self, command, timeout=2.0):
        """Envia um comando para a Aurora e espera o resultado."""
        self.buffer = ""  # Limpa o "teclado/tela" anterior
        self.status = "busy"

        # Adicionamos o marcador no final do comando. 
        # Quando o bash imprimir isso, sabemos que o comando acabou.
        full_command = f"{command} ; echo {MARKER}\n"
        self.process.stdin.write(full_command)
        self.process.stdin.flush()

        return self._esperar_resultado(timeout)

    def send_input(self, text, timeout=2.0):
        """Usado quando o terminal parou para pedir uma resposta (ex: script python)."""
        self.buffer = "" # Limpa a tela
        self.process.stdin.write(text + "\n")
        self.process.stdin.flush()
        self.status = "busy"
        
        return self._esperar_resultado(timeout)

    def _esperar_resultado(self, timeout):
        """Função auxiliar para esperar o marcador ou o tempo limite."""
        start_time = time.time()

        while True:
            # Se achou o marcador, o comando rodou e terminou!
            if MARKER in self.buffer:
                self.status = "free"
                # Limpamos o marcador da string para a Aurora não ver esse "lixo"
                self.buffer = self.buffer.replace(MARKER + "\n", "").replace(MARKER, "")
                break

            # Se demorou mais que o timeout e não vimos o marcador, 
            # provavelmente é um script longo ou ele está travado num 'input()'
            if time.time() - start_time > timeout:
                self.status = "waiting_input"
                break

            time.sleep(0.1) # Pausa pequena para não consumir 100% do seu processador

        return self.buffer.strip()

    def close(self):
        """Mata o processo do terminal."""
        self.process.terminate()

# ==========================================
# ÁREA DE TESTE (Como usar no seu código)
# ==========================================
if __name__ == "__main__":
    t = TerminalSession()
    print("Terminal persistente iniciado. Digite 'sair' para encerrar.\n")

    while True:
        comando = input("[Você] Digite um comando: ")
        
        if comando.lower() == 'sair':
            t.close()
            break

        # Envia o comando e pega a saída
        saida = t.send_command(comando)

        print(f"\n--- [Status: {t.status}] ---")
        print(f"{saida}")
        print("------------------------\n")

        # Se o sistema detectar que não terminou, ele abre chance para input
        while t.status == "waiting_input":
            print("⚠️ O terminal parece estar esperando uma resposta ou rodando algo longo.")
            resposta = input("[Input para o Terminal] (ou aperte Enter para ignorar): ")
            
            if not resposta:
                break
                
            nova_saida = t.send_input(resposta)
            
            print(f"\n--- [Status Atualizado: {t.status}] ---")
            print(f"{nova_saida}")
            print("--------------------------------\n")