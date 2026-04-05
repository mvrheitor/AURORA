import json

def executar_comando(terminal, command):
        output = terminal.send_command(command)
        
        screen = {
            'status': terminal.status,
            'observation': terminal.obs,
            'output': output
        }

        return json.dumps(screen, ensure_ascii=False, indent=4)
    
def enviar_input(terminal, text):
    output = terminal.send_input(text)
    
    screen = {
        'status': terminal.status,
        'observation': terminal.obs,
        'output': output
    }

    return json.dumps(screen, ensure_ascii=False, indent=4)
    
def ler_terminal(terminal):
    output = terminal.read_terminal()

    screen = {
        'status': terminal.status,
        'observation': terminal.obs,
        'output': output
    }

    return json.dumps(screen, ensure_ascii=False, indent=4)
