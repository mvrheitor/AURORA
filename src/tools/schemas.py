tools = [
{
    'type': 'function',
    'function': {
        'name': 'executar_comando',
        'description': 'Executa um comando específico no terminal que está aberto no diretório atual.',
        'parameters': {
            'type': 'object',
            'properties': {
                'command': {
                    'type': 'string',
                    'description': 'O comando a ser executado no sistema. Exemplo: ls -la.'
                }
            },
            'required': ['command'],
        }
    }
},
{
    'type': 'function',
    'function': {
        'name': 'enviar_input',
        'description': 'Se você notar que, após a execução de um comando no terminal, ele ficou esperando por um input, utilize essa função para enviar o input, não a de executar comandos.',
        'parameters': {
            'type': 'object',
            'properties': {
                'text': {
                    'type': 'string',
                    'description': 'O input a ser enviado para o terminal.'
                }
            },
            'required': ['text'],
        }
    }
},
{
    'type': 'function',
    'function': {
        'name': 'ler_terminal',
        'description': 'Mostra o que há na tela do terminal. Como as funções de enviar comandos e inputs para o terminal só mostram o que tinha na tela em um intervalo de 2 segundos, essa função é útil para verificar se a execução do comando já acabou e/ou o que está acontecendo.',
        'parameters': {
            'type': 'object',
            'properties': {},
        }
    }
}
]