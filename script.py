import os
import shutil
import logging
import subprocess


#Configura o módulo logging para mostrar mensagem de nível de informação "INFO"
logging.basicConfig(level = logging.INFO)

def ensure_directory_exists(path):
    #Verifica se o diretório existe. Se não, cria-o.
    if not os.path.exists(path):
        os.makedirs(path)
        logging.info(f"Diretório {path} criado.")

def is_directory_empty_or_nonexistent(path):
    #Verifica se o diretório não existe ou está vazio.
    return not os.path.exists(path) or not os.listdir(path)

def move_item(src_path, dest_path):
    #Move um item (arquivo ou diretório), evitando sobrescrever arquivos existentes.
    if os.path.exists(dest_path):
        logging.warning(f"Destino {dest_path} já existe. Movimentação cancelada.")
        return False

    shutil.move(src_path, dest_path)
    logging.info(f"Arquivo {src_path} movido para {dest_path}.")
    return True

def move_all_items(src_folder, dest_folder):
    #Verifica se o diretório não existe ou está vazio.
    if is_directory_empty_or_nonexistent(src_folder):
        logging.error(f"Pasta de origem {src_folder} não encontrada ou está vazia.")
        return False

    #Verifica se o diretório existe. Se não, cria-o.
    ensure_directory_exists(dest_folder)

    items_moved = 0
    items = os.listdir(src_folder)

    #Para cada file, a função move_file(...) é chamada para tentar mover o arquivo do diretório de origem para o diretório de destino.
    #os.path.join(src_folder, file) cria o caminho completo para o arquivo no diretório de origem.
    #os.path.join(dest_folder, file) cria o caminho completo para onde o arquivo deve ser movido no diretório de destino.
    #Se a função move_file(...) retornar True (indicando que o arquivo foi movido com sucesso), o contador files_moved é incrementado em 1.
    for item in items:
        if move_item(os.path.join(src_folder, item), os.path.join(dest_folder, item)):
            items_moved += 1


    #Retorna True, se o número de arquivos movidos "files_moved" for igual ao número de arquivos presente no diretoria original "len(files)".
    #  Caso contrario retorna False.
    return items_moved == len(items)

def execute_octave():
    #A função subprocess.run() é usada para executar comandos em um subprocesso.
    #O primeiro argumento para subprocess.run() é uma lista que contém o nome do programa a ser executado e seus argumentos (neste caso, o caminho do script Octave)
    #check=True faz com que um subprocess.CalledProcessError seja levantado se o comando retorna um código diferente de zero (o que geralmente indica um erro).
    try:
        result = subprocess.run([r'C:/Users/guisa/OneDrive/Documentos/GitHub/help/Projeto-IA-2023/Octave.lnk', r"--eval", r"run('C:/Users/guisa/OneDrive/Documentos/GitHub/help/Projeto-IA-2023/ia.m')"], shell=True, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        logging.error(f"Erro ao executar o script Octave")
        return False

i = 0
if __name__ == "__main__":
    operations = [
        (r'C:/Users/guisa/OneDrive/Documentos/GitHub/help/Projeto-IA-2023/final', r'C:/Users/guisa/OneDrive/Documentos/GitHub/help/Projeto-IA-2023/banco_base'),
        (r'C:/Users/guisa/OneDrive/Documentos/GitHub/help/Projeto-IA-2023/banco_destino', r'C:/Users/guisa/OneDrive/Documentos/GitHub/help/Projeto-IA-2023/OpenCV')
        #('/caminho/para/sua/pasta/de/origem2', '/caminho/para/sua/pasta/de/destino2')
    ]
    for src, dest in operations:
        match i:
            case 0: 
                #Move da pasta do front para a pasta do octave
                if move_all_items(src, dest):
                    logging.info(f"Items movidos com sucesso de {src} para {dest}")
                else:
                    logging.error(f"Items ao mover alguns ou todos os arquivos de {src} para {dest}")

            case 1: 
                #Executa o octave
                if execute_octave():
                    logging.info("Script Octave executado com sucesso!")

                    # Mova os itens tratados pelo Octave para a pasta de saída
                    if move_all_items(src, dest):
                        logging.info(f"Itens tratados movidos com sucesso de {src} para {dest}")
                    else:
                        logging.error(f"Falha ao mover itens tratados de {src} para {dest}")
                else:
                    logging.error(f"Falha ao executar o script Octave")
        i += 1