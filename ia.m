close all
clear all
clc
pkg load image

## Definição do diretório aqui. Deve ser modificado para maior automatização,
## para que não seja necessário mudar o código para diretórios diferentes.
db_dir = "Banco de Imagens"
ia_manipulation_dir "Banco"

folder_name = readdir(db_dir);

[lin col]=size(folder_name);

for i = 3:lin

  face1 = imread([db_dir '\' folder_name{i}]);

  ##pre-processamento seria feito aqui pra cada imagem
  if isrgb(face1)
    face1=rgb2gray(face1);
  else
    B=A;
  endif


endfor

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
