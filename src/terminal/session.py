import subprocess
import threading
import time
import json

MARKER = "__AURORA_CMD_DONE__" # código pra saber quando um comando terminou

class TerminalSession:
    def __init__(self, shell="/bin/bash"):
        # inicia um terminal de verdade (o bash)
        # subprocess.popen deixa o processo rodando, diferente do .run
        # popen retorna um objeto do processo, não apenas o output
        self.process = subprocess.Popen(
            [shell],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True, # se for falso, vai retornar bits e será necessário converter depois
            bufsize=1 # buffer de linha - menor valor possível para text=True ; faz com que a saída seja liberada linha por linha, o mais rápido possível, sem segurar blocos de texto
        )
        
        self.buffer = "" # a "tela" do terminal ; é aqui que vai ficar o texto da saída
        self.status = "free"  # estados possíveis: 'free', 'busy', 'waiting_input'
        self.obs = "" # observação para AURORA

        # uma thread para ficar lendo o terminal e salvando no buffer:
        self.reader_thread = threading.Thread(target=self._ouvir_terminal, daemon=True)
        self.reader_thread.start()

    def _ouvir_terminal(self):
        # função para ler 1 caractere da saída por vez e ir adicionando ao buffer (a tela) ; 
        while True:
            char = self.process.stdout.read(1)
            if not char:
                break
            self.buffer += char
        # ler um caractere ao invés de uma linha por vez serve para detectar o último output antes de um input que não teve uma quebra de linha. Ex.: input("Digite algo: ")

    def send_command(self, command, timeout=2.0):
        # função para enviar comandos ao terminal
        self.buffer = "" # limpa a "tela", para ler apenas a saída do comando atual
        self.status = "busy" # define o estado como ocupado
        self.obs = ""

        full_command = f"{command} ; echo {MARKER}\n" # envia o comando e retorna o marcador no final do output para sabermos quando o comando acabou
        self.process.stdin.write(full_command) # escreve o comando no input do terminal (stdin)
        self.process.stdin.flush() # força o envio

        return self._esperar_resultado(timeout)

    def send_input(self, text, timeout=2.0):
        # precisamos de uma função separada apenas para enviar texto quando o terminal pede algum input, pois aqui não podemos enviar o echo MARKER
        # ela faz a mesma coisa que a send_command, mas não envia o MARKER
        self.buffer = ""
        self.process.stdin.write(text + "\n")
        self.process.stdin.flush()
        self.status = "busy"
        self.obs = ""
        
        return self._esperar_resultado(timeout)

    def _esperar_resultado(self, timeout):
        # função para ler/verificar a "tela" (o buffer)
        # a função de ouvir o terminal salva a saída no buffer. Esta, por sua vez, verifica o buffer
        start_time = time.time() # define o tempo que começou, para poder parar quando atingir o timeout

        # fica verificando se o nosso marcador já apareceu no buffer
        while True:
            if MARKER in self.buffer:
                self.status = "free" # se estiver, o comando terminou e o terminal está livre
                self.obs = ""
                self.buffer = self.buffer.replace(MARKER + "\n", "").replace(MARKER, "") # remove o marcador da tela, para podermos enviá-la à AURORA sem que ela se confunda
                break
            
            # verifica se o comando está executando a mais tempo do que o limite (timeout) e ainda não apareceu o marcador
            if time.time() - start_time > timeout:
                # se sim, pode ser que o terminal esteja aguardando por um input, ou apenas esteja rodando um comando longo
                self.status = "waiting_input"
                self.obs = "O terminal parece estar esperando uma resposta ou rodando algo longo."
                break # para por causa do timeout e para avisar a AURORA

            time.sleep(0.1) # espera por um décimo de segundo para não consumir 100% da CPU

        return self.buffer.strip() # retorna o que há na tela (buffer)

    def read_terminal(self, timeout=1.0):
        # Uma função para retornar o que há no buffer sem apagar o que tinha antes
        # Somente retorna o que há no buffer se o status == waiting_input, pois se não ele definiria o status como waiting_input mesmo quando estivesse free
        # Se você rodar a função _esperar_resultado quando o status é free, ou seja, quando o marcador já passou pelo buffer e foi removido, ela verificará se o marcador está no buffer, não o encontrará e definirá o status para waiting_input
        if self.status == "waiting_input":
            return self._esperar_resultado(timeout)
        else:
            return ""
        # Foi necessário desenvolver essa função para eliminar "pontos cegos", ou seja, respostas de inputs que demoram mais que o timeout
            
    
    def close(self):
        # uma função para fechar o terminal. Porque sim.
        self.process.terminate()


if __name__ == "__main__":
    t = TerminalSession()

    def executar_comando(command):
        output = t.send_command(command)
        
        screen = {
            'status': t.status,
            'observation': t.obs,
            'output': output
        }

        return json.dumps(screen, indent=4)
    
    def enviar_input(text):
        output = t.send_input(text)
        
        screen = {
            'status': t.status,
            'observation': t.obs,
            'output': output
        }

        return json.dumps(screen, indent=4)
    
    def ler_terminal():
        output = t.read_terminal()

        screen = {
            'status': t.status,
            'observation': t.obs,
            'output': output
        }

        return json.dumps(screen, indent=4)

    

    while True:
        print("[1] - Enviar comando")
        print("[2] - Enviar input")
        print("[3] - Ler terminal")
        escolha = int(input("Escolha uma opção: "))
        

        if escolha == 1:
            comando = input("Digite o comando: ")
            screen = executar_comando(comando)
            print(screen)
        elif escolha == 2:
            text = input("Digite o input: ")
            screen = enviar_input(text)
            print(screen)
        elif escolha == 3:
            print(ler_terminal())