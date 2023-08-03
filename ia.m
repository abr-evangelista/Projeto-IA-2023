close all
clear all
clc
pkg load image

## Definição do diretório aqui. Deve ser modificado para maior automatização,
## para que não seja necessário mudar o código para diretórios diferentes.
db_dir = "banco_base";
ia_manipulation_dir = "banco_destino";

folder_name = readdir(db_dir);

[lin col]=size(folder_name);

for i = 3:lin

  face1 = imread([db_dir '\' folder_name{i}]);

  ## pre-processamento seria feito aqui pra cada imagem
  if isrgb(face1)
    face1 = rgb2gray(face1);
  else
    face1 = face1;
  endif

  ## Salvamento de cada nova imagem na pasta destino. O format da imagem depende
  ## do que vc colocar como final da string na linha de imwrite, mas deve ser um
  ## formato suportado pelo Octave (cheque com o comando imformats no Shell do
  ## Octave).
  imwrite(face1, [ia_manipulation_dir '\' "image" num2str(i-2) ".png"]);

endfor

## Script pra pequeno teste, puxando uma imagem salva do folder de destino e
## vendo se ela foi salva corretamente e pode ser lida.
##A = imread([ia_manipulation_dir '\' "image1"]);
##
##figure, imshow(A);

%%%%%%%%%%
## Aqui, alguns testes estavam sendo feitos pra decidir que tecnicas de
## pré-processamento usariamos
##A = imread("test.jpg");
##
##figure, imhist(A);
##
##A = rgb2gray(A);
##
##A = ~im2bw(A, 0.5);
##
##figure, imshow(A);
##
##A2 = bwmorph(A, 'thin', Inf);
##
##figure, imshow(A2);
##
##B = imread("test2.jpg");
##
##figure, imhist(B);
##
##B = rgb2gray(B);
##
##figure, imhist(B);
##
##B = ~im2bw(B, 0.5);
##
##figure, imshow(B);
##
##B2 = bwmorph(B, 'thin', Inf);
##
##figure, imshow(B2);
##
##C = imread("test3.jpg");
##
##C = rgb2gray(C)
##
##figure, imhist(C);
##
##figure, imshow(C);
##
##C = ~im2bw(C, 0.2);
##
##figure, imshow(C);
##
##C2 = bwmorph(C, 'thin', Inf);
##
##figure, imshow(C2);
##
##D = imread("test4.jpg");
##
##D = rgb2gray(D);
##
##figure, imhist(D);
##
##figure, imshow(D);
##
##D = ~im2bw(D, 0.56);
##
##figure, imshow(D);
##
##D2 = bwmorph(D, 'thin', Inf);
##
##figure, imshow(D2);
%%%%%%%%%%
