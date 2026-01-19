import json
import subprocess

def pwd_ls():
    caminho = subprocess.run(['pwd'], stdout=subprocess.PIPE, text=True, check=True).stdout
    conteudo = subprocess.run(['ls', '-la'], stdout=subprocess.PIPE, text=True, check=True).stdout
    return json.dumps({'path': caminho, 'content': conteudo})

def criar_pasta(path='./pasta_sem_nome'):
    try:
        saida = subprocess.run(['mkdir', path], stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True, check=True)
        return json.dumps({'ok': True, 'message': f'Directory {path} created successfully'})
    except subprocess.CalledProcessError as e:
        return json.dumps({'ok': False, 'error': e.stderr})

def criar_arquivo(path='./untitled'):
    try:
        saida = subprocess.run(['touch', path], stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True, check=True)
        return json.dumps({'ok': True, 'message': f'File {path} created successfully'})
    except subprocess.CalledProcessError as e:
        return json.dumps({'ok': False, 'error': e.stderr})