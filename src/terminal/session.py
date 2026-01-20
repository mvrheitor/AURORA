import subprocess
import threading # pra poder usar/ouvir o terminal enquanto executa o resto do programa
import queue # necessário nesse caso para evitar race condition

MARKER = "__AURORA_CMD_DONE__"

class TerminalSession:
    def __init__(self):
        self.process = subprocess.Popen(
            ["/bin/bash"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        self.output_queue = queue.Queue() # cria uma caixa/fila vazia para armazenar a saída
        self.reader_thread = threading.Thread(target=self._ler_saida, daemon=True)
        self.reader_thread.start() # fica escutando a saída do shell assim que ele é criado

    def send(self, comando):
        self.process.stdin.write(f"{comando} && echo {MARKER}\n") # o bash só executa se der Enter
        self.process.stdin.flush() # força o comando a ser enviado (as vezes fica esperando)
    def _ler_saida(self):
        for linha in self.process.stdout:
            self.output_queue.put(linha)
    def read_output(self):
        saidas = []
        while not self.output_queue.empty():
            saidas.append(self.output_queue.get())
        return "".join(saidas)




t = TerminalSession()

while True:
    comando = str(input())
    t.send(comando)
    escolha = int(input("1 - ler\n 2 - enviar outro comando"))
    while escolha == 1:
        print(t.read_output())
        escolha = int(input("1 - ler\n 2 - enviar outro comando"))
