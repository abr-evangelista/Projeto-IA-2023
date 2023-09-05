import json
import os

dir = 'banco_label_master'
dicionario = {}

diretorio = os.listdir(dir)
tupla = []

def get_number(file_name):
    return int(file_name.split(".")[0].split("image")[1])

# Create a list of tuples containing the filenames and their numeric parts
for file in diretorio:
    aux = (file, get_number(file))
    tupla.append(aux)

# Sort the list of tuples based on the numeric part
sortedDir = sorted(tupla, key=lambda x: x[1])

# Populate the 'final' list with sorted filenames
final = [tup[0] for tup in sortedDir]

# Create the dictionary using 'final' list
for i, file in enumerate(final):
    path = os.path.join(dir, file)
    with open(path, 'r') as ajuda:
        dicionario[f'imagem{i+1}'] = json.load(ajuda)

# Save the dictionary as a JSON file
with open(os.path.join(dir, 'imagens.json'), 'w') as json_file:
    json.dump(dicionario, json_file, indent=1)
