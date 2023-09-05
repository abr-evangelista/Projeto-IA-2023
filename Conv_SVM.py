import cv2
import numpy as np
import json
import os

# Função para carregar os dados das anotações
def load_annotations(json_path):
    with open(json_path, 'r') as file:
        data = json.load(file)
    return data

# Função para calcular o centroide de um contorno
def get_centroid(contour):
    M = cv2.moments(contour)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
    else:
        cx, cy = 0, 0
    return cx, cy

# Diretórios
src_directory = "C:/Users/guisa/OneDrive/Documentos/GitHub/help/Projeto-IA-2023/banco_label_master"  # Caminho para o diretório com os arquivos JSON originais
dest_directory = "C:/Users/guisa/OneDrive/Documentos/GitHub/help/Projeto-IA-2023/anotacao"  # Caminho para o diretório onde os resultados serão salvos

# Lista todos os arquivos no diretório e filtra apenas os arquivos .json
json_files = [f for f in os.listdir(src_directory) if f.endswith('.json')]

for json_file in json_files:
    # Carregando os dados
    annotations_path = os.path.join(src_directory, json_file)
    annotations = load_annotations(annotations_path)

    mouth_contours = annotations["guardarContornoBoca"]
    mouth_centroids = [get_centroid(np.array(contour)) for contour in mouth_contours]
    
    # Salvando os resultados no diretório de destino
    output_data = {
        "mouth_centroids": mouth_centroids
    }
    output_path = os.path.join(dest_directory, json_file)
    with open(output_path, 'w') as output_file:
        json.dump(output_data, output_file, indent=2)
