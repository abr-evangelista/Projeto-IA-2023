import cv2
import numpy as np
import os
import json
import dlib


#Ao criar um objeto desta classe, os detectores de face do Dlib são inicializados. 
# O HOG, que é um método de extração de características, também é configurado com parâmetros específicos.
class FaceDetector:

#1    
##############################################################################################################################################################################
    
    #A biblioteca Dlib possui uma função chamada get_frontal_face_detector(), que retorna um detector de rostos frontal pré-treinado.
    
    #shape_predictor que pode ser usada para prever landmarks (ou pontos-chave) em um rosto, como a posição dos olhos, nariz e boca.
    #Para funcionar corretamente, o shape_predictor precisa de um modelo treinado. 
    # O arquivo "shape_predictor_68_face_landmarks.dat" é esse modelo treinado, que permite prever 68 pontos-chave em um rosto.
    
    #Aqui, a função privada _init_hog() da classe é chamada para configurar e retornar um descritor HOG (Histogram of Oriented Gradients).
    
    def __init__(self):
        self.detector_dlib = dlib.get_frontal_face_detector()
        self.predictor_dlib = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        self.hog = self._init_hog()

##############################################################################################################################################################################
   
#2   
##############################################################################################################################################################################
    #Configura e retorna um descritor HOG.
    
    #winSize=(64, 64): é o tamanho da janela de detecção. A janela de detecção é a região na imagem onde a busca é realizada.
    
    #blockSize = (16, 16): define o tamanho do bloco em pixels. Em HOG, a imagem é dividida em pequenos blocos quadrados (ou retangulares).
    # Cada bloco é então normalizado, o que ajuda na melhoria da precisão da detecção.
    
    #blockStride = (8, 8): define o passo da célula em pixels. 
    # Ao calcular o HOG para a imagem, movemos a janela de bloco ao longo da imagem e calculamos o HOG para cada posição.
    # O blockStride determina o número de pixels que a janela de bloco se move para a próxima posição.
    
    # cellSize = (8, 8): Define o tamanho das células que compõem cada bloco. Neste caso, cada célula tem 8x8 pixels.
    
    #nbins = 9: Define o número de bins (intervalos) para o histograma de orientações usado no cálculo do HOG.
    
    #A função cv2.HOGDescriptor é usada para criar uma instância do descritor HOG.
    
    def _init_hog(self, winSize=(64, 64)):
        blockSize = (16, 16)
        blockStride = (8, 8)
        cellSize = (8, 8)
        nbins = 9
        return cv2.HOGDescriptor(winSize, blockSize, blockStride, cellSize, nbins)

    @staticmethod
    # Realiza a pré-processamento da imagem - redimensiona para um tamanho especificado e converte para escala de cinza.
    def preprocess_image(img, winSize=(64, 64)):
        return cv2.cvtColor(cv2.resize(img, winSize), cv2.COLOR_BGR2GRAY)


##############################################################################################################################################################################
    
#3    
##############################################################################################################################################################################    
    #Usa um modelo SVM treinado para detectar a boca em uma imagem.
    
    #h = self.hog.compute(gray_image): Utiliza o descritor HOG, que foi inicializado e configurado anteriormente (pelo método _init_hog), 
    # para calcular o vetor de características HOG da imagem em escala de cinza. O resultado é armazenado na variável h.
    
    #_, pred = svm.predict(h.reshape(1, -1)): O vetor de características HOG h é remodelado para se ajustar à entrada esperada do modelo SVM e, 
    # em seguida, é usado para fazer uma predição usando o modelo SVM fornecido
    #A função svm.predict retorna dois valores. O primeiro valor (denotado aqui por _) é um código de status que indica o sucesso ou falha da operação de predição. 
    #O segundo valor, pred, é a predição real feita pelo modelo, que neste contexto representa as coordenadas do retângulo da boca.
    
    #return pred[0]: Finalmente, o método retorna o primeiro item da predição, que é o retângulo (coordenadas e dimensões) da boca detectada na imagem.
    
    
            #-----------------------------------------------------------
            #Explicação:
            #Para simplificar, esta função pega uma imagem facial como entrada, processa-a, extrai suas características usando HOG, 
            # e então usa um modelo SVM treinado para detectar a localização da boca na imagem. A localização detectada da boca é então retornada como uma saída.
            
            #-----------------------------------------------------------
            
    def svm_detection(self, image, svm):
        gray_image = self.preprocess_image(image)
        h = self.hog.compute(gray_image)
        _, pred = svm.predict(h.reshape(1, -1))
        return pred[0]


##############################################################################################################################################################################    

#4
##############################################################################################################################################################################    

   # Usa o detector Dlib para detectar landmarks faciais. Retorna as coordenadas relacionadas à boca.
   
   #detections = self.detector_dlib(gray_image): O detector frontal de face do Dlib é usado para encontrar todas as faces presentes na imagem em escala de cinza. 
   # Cada detecção é um retângulo que indica a localização da face na imagem.
   
   #mouth_coords = []: Uma lista vazia é inicializada para armazenar as coordenadas da boca detectadas em todas as faces encontradas.
   
   #shape = self.predictor_dlib(gray_image, detection): Para cada face detectada, o preditor do Dlib é usado para identificar 68 landmarks faciais. 
   # Estes landmarks representam pontos chave no rosto, como os cantos dos olhos, o nariz, etc.
   
   #mouth_dlib = shape.parts()[48:68]: Os pontos de 48 a 67 (68 não incluso) dos landmarks representam as coordenadas ao redor da boca. 
   # Estas coordenadas são extraídas e armazenadas na variável mouth_dlib.
   
            #------------------------------------------------------------------
            #Explicação:
            #Pontos 48 a 59 definem o contorno externo dos lábios.
            #Pontos 60 a 67 definem o contorno interno dos lábios (a linha onde os lábios se encontram quando a boca está fechada).
            
            #A decisão de usar esses pontos específicos provém da forma como o modelo de 68 pontos foi treinado e da estrutura anatômica padrão dos rostos humanos.
            # A biblioteca dlib utiliza este modelo de landmarks específico para identificar e marcar pontos-chave no rosto.
            
            #------------------------------------------------------------------
    
    #mouth_coords.append(mouth_dlib): As coordenadas da boca são adicionadas à lista mouth_coords.
    
    #return mouth_coords: Após processar todas as faces detectadas, o método retorna a lista de coordenadas da boca.
            #------------------------------------------------------------------
            #Em resumo:
            #esta função leva uma imagem facial como entrada, detecta todas as faces presentes nessa imagem usando o Dlib, e para cada face detectada, 
            #identifica e retorna as coordenadas ao redor da boca.
            
            #------------------------------------------------------------------
    
    
    def dlib_detection(self, image):
        gray_image = self.preprocess_image(image)
        detections = self.detector_dlib(gray_image)
        mouth_coords = []
        for detection in detections:
            shape = self.predictor_dlib(gray_image, detection)
            mouth_dlib = shape.parts()[48:68]
            mouth_coords.append(mouth_dlib)
        return mouth_coords

##############################################################################################################################################################################

#5
##############################################################################################################################################################################
#Carrega imagens de um diretório e suas respectivas anotações (coordenadas da boca) a partir de um arquivo JSON.
def load_data(image_dir, annotations_file):
    images = []
    mouth_rects = []
    image_filenames = [f for f in os.listdir(image_dir) if f.endswith('.jpg')]
    
    with open(annotations_file, 'r') as f:
        filename_to_annotation = json.load(f)
    
    for filename in image_filenames:
        img_path = os.path.join(image_dir, filename)
        if os.path.exists(img_path):
            img = cv2.imread(img_path)
            images.append(img)
            annotation = filename_to_annotation.get(filename, {})
            mouth_rects.append((annotation.get("x", 0), 
                                annotation.get("y", 0),
                                annotation.get("w", 0),
                                annotation.get("h", 0)))
    return images, mouth_rects

#Para cada imagem, ela é pré-processada e as características são extraídas usando o descritor HOG.

##############################################################################################################################################################################

#6
##############################################################################################################################################################################

            #------------------------------------------------------------------
            #Objetivo:
            #Extrair características (especificamente usando o descritor HOG - Histogram of Oriented Gradients) de uma lista de imagens 
            # e retornar essas características juntamente com os rótulos correspondentes.
            
            #------------------------------------------------------------------
    
    #training_data e labels:inicializa duas listas vazias: uma para armazenar os dados de características extraídas e outra para os rótulos correspondentes.
    
    #Loop for image, rect in zip(images, mouth_rects):
    #Itera sobre cada imagem e seu retângulo de boca correspondente (que representa a localização da boca na imagem).
    
    #image = detector.preprocess_image(image, winSize): Pré-processa
    
    #h = detector.hog.compute(image): Calcula o descritor HOG para a imagem pré-processada. 
    # Este descritor captura informações de borda e textura que são úteis para tarefas de detecção e reconhecimento.
    
    #training_data.append(h):Adiciona o descritor HOG calculado à lista training_data.
    
    #labels.append(list(rect)): Converte o retângulo da boca (que é uma tupla) para uma lista e a adiciona à lista labels.
    
    #Return...: Converte as listas training_data e labels para arrays numpy de tipo float32 e as retorna.
def extract_features(images, mouth_rects, detector, winSize=(64, 64)):
    training_data = []
    labels = []

    for image, rect in zip(images, mouth_rects):
        image = detector.preprocess_image(image, winSize)
        h = detector.hog.compute(image)
        training_data.append(h)
        labels.append(list(rect)) 

    return np.array(training_data, np.float32), np.array(labels, np.float32)

##############################################################################################################################################################################

#7
##############################################################################################################################################################################

    #Usa os dados de treinamento fornecidos (características HOG) para treinar um modelo SVM que, posteriormente, pode ser usado para detecção.

    #SVM_create: Cria um novo objeto SVM vazio usando a biblioteca OpenCV.

    #setType: Define o tipo de SVM como C-SVC. C-SVC é um tipo de SVM para classificação.

    #setKernel: Define o tipo de kernel do SVM como linear. O kernel determina a função usada para encontrar o hiperplano de separação no espaço de características. 
    # Um kernel linear tenta encontrar um hiperplano linear para separar as classes.

    #setTermCriteria: Define os critérios de parada do treinamento do SVM.
    #cv2.TERM_CRITERIA_MAX_ITER indica que o treinamento será interrompido após um número máximo de iterações(100). 1e-6 é a precisão desejada.

    #svm.train: Treina o modelo SVM usando os dados de treinamento e rótulos fornecidos.   
    #training_data: As características extraídas das imagens (por exemplo, usando o descritor HOG).
    #cv2.ml.ROW_SAMPLE: Indica que cada linha de training_data representa uma amostra.
    #labels: Os rótulos correspondentes para cada amostra em training_data.

            #------------------------------------------------------------------
            #Explicação:
            # Utiliza um algoritmo de otimização (por exemplo, a técnica de otimização de Lagrange)
            # para encontrar o hiperplano que maximiza a margem entre os vetores de suporte das duas classes. 
            
            #------------------------------------------------------------------
def train_svm(training_data, labels):
    svm = cv2.ml.SVM_create()
    svm.setType(cv2.ml.SVM_C_SVC)
    svm.setKernel(cv2.ml.SVM_LINEAR)
    svm.setTermCriteria((cv2.TERM_CRITERIA_MAX_ITER, 100, 1e-6))
    svm.train(training_data, cv2.ml.ROW_SAMPLE, labels)
    return svm


##############################################################################################################################################################################


def main():
    detector = FaceDetector()

    # Load and train
    images, mouth_rects = load_data("images", "annotations.json")
    training_data, labels = extract_features(images, mouth_rects, detector)
    svm = train_svm(training_data, labels)

    # Process test image
    test_image_path = "path_to_your_test_image.jpg"
    if os.path.exists(test_image_path):
        test_image = cv2.imread(test_image_path)
        print("SVM Detection:", detector.svm_detection(test_image, svm))
        print("Dlib Mouth Coords:", detector.dlib_detection(test_image))
    else:
        print(f"Error: {test_image_path} does not exist!")


if __name__ == '__main__':
    main()
