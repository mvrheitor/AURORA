import subprocess
import threading  # pra poder usar/ouvir o terminal enquanto executa o resto do programa
import queue  # necessário nesse caso para evitar race condition
import json
import selectors
import os
import time
import fcntl

MARKER = "__AURORA_CMD_DONE__"

class TerminalSession:
    def __init__(self, shell="/bin/bash", input_wait_seconds=1.0):
        self.process = subprocess.Popen(
            [shell],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=0
        )
        self.status = {
            'status': 'free',
            'observation': 'The terminal is free to receive inputs.',
            'last_output': None,
            'waiting_for_input': False
        }
        self.output_queue = queue.Queue()  # cria uma caixa/fila vazia para armazenar a saída
        self._selector = selectors.DefaultSelector()
        self._stdout_buffer = ""
        self._last_output_ts = time.time()
        self._input_wait_seconds = input_wait_seconds
        self._setup_nonblocking_io()
        self.reader_thread = threading.Thread(target=self._ler_saida, daemon=True)
        self.reader_thread.start()  # fica escutando a saída do shell assim que ele é criado

    def send(self, comando):
        self.process.stdin.write(f"{comando} ; echo {MARKER}\n".encode("utf-8"))  # executa mesmo que o primeiro comando dê erro
        self.process.stdin.flush()  # força o comando a ser enviado (as vezes fica esperando)
        self.status['status'] = 'busy'
        self.status['observation'] = 'The terminal is currently executing a command. Please wait.'
        self.status['waiting_for_input'] = False
        return "Command sent. Please, verify terminal."

    def send_input(self, texto):
        self.process.stdin.write(f"{texto}\n".encode("utf-8"))
        self.process.stdin.flush()
        self.status['waiting_for_input'] = False
        return "Input sent."

    def _setup_nonblocking_io(self):
        for stream in (self.process.stdout, self.process.stderr):
            fd = stream.fileno()
            flags = fcntl.fcntl(fd, fcntl.F_GETFL)
            fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)
        self._selector.register(self.process.stdout, selectors.EVENT_READ, data="stdout")
        self._selector.register(self.process.stderr, selectors.EVENT_READ, data="stderr")

    def _handle_stdout(self, texto):
        self._stdout_buffer += texto
        marker_index = self._stdout_buffer.find(MARKER)
        if marker_index != -1:
            before = self._stdout_buffer[:marker_index]
            after = self._stdout_buffer[marker_index + len(MARKER):]
            if after.startswith("\n"):
                after = after[1:]
            if before:
                self.output_queue.put(before)
                self.status['last_output'] = before
            self._stdout_buffer = after
            self.status['status'] = 'free'
            self.status['observation'] = 'The terminal is free to receive inputs.'
            self.status['waiting_for_input'] = False
        else:
            if texto:
                self.output_queue.put(texto)
                self.status['last_output'] = texto

    def _ler_saida(self):
        while True:
            events = self._selector.select(timeout=0.1)
            if not events:
                if self.status['status'] == 'busy':
                    if (time.time() - self._last_output_ts) >= self._input_wait_seconds:
                        self.status['waiting_for_input'] = True
                        self.status['observation'] = 'Program may be waiting for input.'
                continue
            for key, _ in events:
                stream_name = key.data
                try:
                    data = os.read(key.fileobj.fileno(), 4096)
                except OSError:
                    data = b""
                if not data:
                    continue
                texto = data.decode("utf-8", errors="replace")
                self._last_output_ts = time.time()
                if stream_name == "stdout":
                    self._handle_stdout(texto)
                else:
                    prefixed = f"[stderr] {texto}"
                    self.output_queue.put(prefixed)
                    self.status['last_output'] = prefixed
    def read_output(self):
        saidas = []
        while not self.output_queue.empty():
            saidas.append(self.output_queue.get())  # pega todas as linhas do output que estavam na fila e coloca em uma lista
        return "".join(saidas)  # retorna as linhas um em baixo da outra, por isso tem que ser .join
    def verify_terminal_status(self):
        return json.dumps(self.status)

    def close(self):
        try:
            self.process.terminate()
        except Exception:
            pass


if __name__ == "__main__":
    t = TerminalSession()

    while True:
        comando = str(input())
        t.send(comando)
        escolha = int(input("1 - ler\n2 - enviar outro comando\n3 - Status\n4 - enviar input\n"))
        while escolha == 1:
            print(t.read_output())
            escolha = int(input("1 - ler\n2 - enviar outro comando\n3 - Status\n4 - enviar input\n"))
        while escolha == 3:
            print(t.verify_terminal_status())
            escolha = int(input("1 - ler\n2 - enviar outro comando\n3 - Status\n4 - enviar input\n"))
        while escolha == 4:
            resposta = str(input("Input: "))
            t.send_input(resposta)
            escolha = int(input("1 - ler\n2 - enviar outro comando\n3 - Status\n4 - enviar input\n"))
