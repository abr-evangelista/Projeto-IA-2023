close all;
clear all;
clc;
pkg load image;

#Definição do diretório aqui. Deve ser modificado para maior automatização,
#para que não seja necessário mudar o código para diretórios diferentes.
db_dir = "final";
ia_manipulation_dir = "imagem_aux";

folder_name = readdir(db_dir);

[line colm]=size(folder_name);

for count = 3:line

  ## algo aqui embaixo deve ser feito para evitar sobreposição de imagens com
  ## tamanhos diferentes. provavelmente deve ser feito pra toda variavel "face"
  ## antes de ser usada na função.
  face1 = 0;

  name = folder_name{count};
  face1 = imread([db_dir '/' name]);

  ## pre-processamento seria feito aqui pra cada imagem
  if isrgb(face1)
    face1 = rgb2gray(face1);
  else
    face1 = face1;
  endif

  ## suavização por mediana, tirando alguns ruidos problematicos da imagem.
  face2 = medfilt2(face1, [3 3]);

  ## essa função nos traz uma imagem com bordas binarizadas em relação ao resto.
  face3 = edge(face2, 'Canny');

  ## Salvamento de cada nova imagem na pasta destino. O format da imagem depende
  ## do que vc colocar como final da string na linha de imwrite, mas deve ser um
  ## formato suportado pelo Octave (cheque com o comando imformats no Shell do
  ## Octave).
  figure;
  imwrite(face3, [ia_manipulation_dir '/' name]);
  close all;

endfor