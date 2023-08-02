close all
clear all
clc
pkg load image

folder_name = readdir("Banco de Imagens")

[lin col]=size(folder_name);

for i = 3:lin
  printf(folder_name{i});
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
##figure, imhist(C);
##
##C = rgb2gray(C);
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



