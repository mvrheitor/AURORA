import subprocess
import threading
import time

MARKER = "__AURORA_CMD_DONE__"

class TerminalSession:
    def __init__(self, shell="/bin/bash"):
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

        self.reader_thread = threading.Thread(target=self._ouvir_terminal, daemon=True)
        self.reader_thread.start()

    def _ouvir_terminal(self):
        while True:
            char = self.process.stdout.read(1)
            if not char:
                break
            self.buffer += char

    def send_command(self, command, timeout=2.0):
        self.buffer = ""
        self.status = "busy"

        full_command = f"{command} ; echo {MARKER}\n"
        self.process.stdin.write(full_command)
        self.process.stdin.flush()

        return self._esperar_resultado(timeout)

    def send_input(self, text, timeout=2.0):
        self.buffer = ""
        self.process.stdin.write(text + "\n")
        self.process.stdin.flush()
        self.status = "busy"
        
        return self._esperar_resultado(timeout)

    def _esperar_resultado(self, timeout):

        start_time = time.time()

        while True:
            if MARKER in self.buffer:
                self.status = "free"
                self.buffer = self.buffer.replace(MARKER + "\n", "").replace(MARKER, "")
                break

            if time.time() - start_time > timeout:
                self.status = "waiting_input"
                break

            time.sleep(0.1)

        return self.buffer.strip()

    def close(self):
        self.process.terminate()


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

        while t.status == "waiting_input":
            print("⚠️ O terminal parece estar esperando uma resposta ou rodando algo longo.")
            resposta = input("[Input para o Terminal] (ou aperte Enter para ignorar): ")
            
            if not resposta:
                break
                
            nova_saida = t.send_input(resposta)
            
            print(f"\n--- [Status Atualizado: {t.status}] ---")
            print(f"{nova_saida}")
            print("--------------------------------\n")