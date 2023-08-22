close all
clear all
clc
pkg load image

## Definição do diretório aqui. Deve ser modificado para maior automatização,
## para que não seja necessário mudar o código para diretórios diferentes.
db_dir = "banco_base";
ia_manipulation_dir = "banco_destino";

folder_name = readdir(db_dir);

[line colm]=size(folder_name);

for count = 3:line

  ## algo aqui embaixo deve ser feito para evitar sobreposição de imagens com
  ## tamanhos diferentes. provavelmente deve ser feito pra toda variavel "face"
  ## antes de ser usada na função.
  face1 = 0;

  face1 = imread([db_dir '\' folder_name{count}]);

  ## pre-processamento seria feito aqui pra cada imagem
  if isrgb(face1)
    face1 = rgb2gray(face1);
  else
    face1 = face1;
  endif

  ## suavização por mediana, tirando alguns ruidos problematicos da imagem.
  size_template = 3;

  [lin col] = size(face1);

  for i = 2 : (lin-fix(size_template/2))
      for j = 2 : (col - fix(size_template/2))
          k = 1;
          for m = i - 1 : i + 1
              for n = j - 1 : j + 1
                  vetor_elem_mediana(k) = face1(m,n);
                  k = k + 1;
              end
          end
          vetor_elem_mediana = sort(vetor_elem_mediana);
          face2(i,j) = vetor_elem_mediana(fix(length(vetor_elem_mediana)/2) + 1);
      end
  end

  ## essa função nos traz uma imagem com bordas binarizadas em relação ao resto.
  face3 = edge(face2, 'Canny');

  ## Salvamento de cada nova imagem na pasta destino. O format da imagem depende
  ## do que vc colocar como final da string na linha de imwrite, mas deve ser um
  ## formato suportado pelo Octave (cheque com o comando imformats no Shell do
  ## Octave).
  imwrite(face3, [ia_manipulation_dir '\' "image" num2str(count-2) ".png"]);

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
