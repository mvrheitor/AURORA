tools = [
    {
    'type': 'function',
    'function': {
        'name': 'pwd_ls',
        'description': 'Executa os comandos "pwd" e "ls -la" no sistema, ou seja, mostra o diretório atual e o conteúdo dentro dele.',
        'parameters': {
            'type': 'object',
            'properties': {}
        }
    }
},
{
    'type': 'function',
    'function': {
        'name': 'criar_pasta',
        'description': 'Cria uma nova pasta em um diretório específico.',
        'parameters': {
            'type': 'object',
            'properties': {
                'path': {
                    'type': 'string',
                    'description': 'O caminho completo da pasta a ser criada. Exemplo: /path/to/new_folder1. Se não especificado, criará o diretório "./pasta_sem_nome".'
                    }
                },
            }
        }
},
{
    'type': 'function',
    'function': {
        'name': 'criar_arquivo',
        'description': 'Cria um novo arquivo em um diretório específico.',
        'parameters': {
            'type': 'object',
            'properties': {
                'path': {
                    'type': 'string',
                    'description': 'O caminho completo do arquivo a ser criada. Exemplo: /path/to/new_file.txt. Se não especificado, criará o arquivo "./untitled".'
                    }
                },
            }
        }
}
]