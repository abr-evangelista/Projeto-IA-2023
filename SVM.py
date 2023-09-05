import cv2
import numpy as np
import os
import json
import json.decoder
import dlib
import matplotlib.pyplot as plt



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
    def preprocess_image(img, winSize=None):
        if winSize:
            img = cv2.resize(img, winSize)
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


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
            
    def svm_detection(self, image, svm_x, svm_y):
        # Assegurar que a imagem de teste é redimensionada para o mesmo tamanho de janela
        winSize = (64, 64)
        image = cv2.resize(image, winSize)
        gray_image = self.preprocess_image(image, winSize)
        h = self.hog.compute(gray_image)

        # Print the shape of HOG descriptor
        print("Shape of HOG descriptor:", h.shape)

        # Ensure the datatype is float32
        h = h.astype(np.float32)
        
        x_pred = svm_x.predict(h.reshape(1, -1))[1][0][0]
        y_pred = svm_y.predict(h.reshape(1, -1))[1][0][0]
        return x_pred, y_pred

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
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Apenas convertendo para escala de cinza, sem redimensionamento.
        detections = self.detector_dlib(gray_image, 1)  # Adicionando upsample para melhor detecção.
        if not detections:
            print("Nenhuma face detectada pela Dlib na imagem.")
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
import os
import json
import cv2

def load_data(image_dir: str, json_dir: str) -> (list, list):
    images = []
    mouth_contours = []

    # Lista todos os arquivos de imagem no diretório
    image_files = [f for f in os.listdir(image_dir) if f.endswith('.png')]

    for img_filename in image_files:
        base_name, _ = os.path.splitext(img_filename)  # Extrai o nome base da imagem (sem a extensão)
        json_path = os.path.join(json_dir, base_name + '.json').replace("//", "/")
        
        # Tenta carregar o arquivo JSON com as anotações
        try:
            with open(json_path, 'r') as f:
                annotation = json.load(f)
            
            # Verifica se o arquivo JSON está vazio ou não contém a chave desejada
            if not annotation or "mouth_centroids" not in annotation or not annotation["mouth_centroids"]:
                print(f"Arquivo JSON {json_path} está vazio ou não contém anotações de contorno de boca. Pulando.")
                continue

            # Verifica se os dados são listas de pontos
            mouth_data = annotation["mouth_centroids"]
            if not all(isinstance(pt, (list, tuple)) and len(pt) == 2 for pt in mouth_data):
                print(f"Contorno de boca no arquivo {json_path} não está no formato esperado (x, y). Pulando.")
                continue

            contour = mouth_data[0]
            if isinstance(contour, list) and len(contour) == 2:
                x, y = contour

                if isinstance(x, int) and isinstance(y, int):
                    mouth_contours.append((x, y))
                else:
                    print(f"Tipo de 'contour': {type(contour)}")
                    print(f"Contorno problemático: {contour}")
                    print(f"Tipo de 'point x': {type(x)}")
                    print(f"Tipo de 'point y': {type(y)}")
                    continue
            else:
                print(f"Tipo de 'contour': {type(contour)}")
                print(f"Contorno problemático: {contour}")
                continue

        except (IOError, json.JSONDecodeError) as e:
            print(f"Erro ao carregar o arquivo JSON {json_path}. Detalhes: {e}. Pulando.")
            continue

        img_path = os.path.join(image_dir, img_filename).replace("//", "/")
        img = cv2.imread(img_path)

        # Verifica se o arquivo de imagem está vazio
        if img is None or img.size == 0:
            print(f"Erro ao carregar imagem {img_path} ou imagem vazia. Pulando.")
            continue

        images.append(img)

    print(f"Carregadas {len(images)} imagens e {len(mouth_contours)} anotações de boca.")
    
    return images, mouth_contours




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
def extract_features(images, mouth_contours, detector, winSize=(64, 64)):
    training_data = []
    labels_x = []
    labels_y = []

    total_contours = 0
    valid_contours = 0
    invalid_contours = 0
    
    i = 0
    while i < len(images):
        total_contours += 1
        contour = mouth_contours[i]
        print(f"Tipo de 'contour': {contour}")

        # Ajuste na verificação do contorno
        if isinstance(contour, tuple) and len(contour) == 2 and all(isinstance(coord, (int, float)) for coord in contour):
            try:
                image = images[i]
                image = detector.preprocess_image(image, winSize)
                h = detector.hog.compute(image)
                training_data.append(h)

                # Calcula os centroides
                centroid_x = contour[0]
                centroid_y = contour[1]
                valid_contours += 1

                # Adiciona os centroides às listas de rótulos
                labels_x.append(centroid_x)
                labels_y.append(centroid_y)
                i += 1
                
            except ValueError as e:
                print(f"Erro ao extrair características para uma imagem. Detalhes: {e}")
                # Removendo a imagem e o contorno inválido
                images.pop(i)
                mouth_contours.pop(i)
                invalid_contours += 1
        else:
            print("Contorno problemático:", contour)
            # Removendo a imagem e o contorno inválido
            images.pop(i)
            mouth_contours.pop(i)
            invalid_contours += 1

    print(f"Total de contornos: {total_contours}")
    print(f"Contornos válidos: {valid_contours}")
    print(f"Contornos inválidos: {invalid_contours}") 
    
    return np.array(training_data, np.float32), np.array(labels_x, np.float32), np.array(labels_y, np.float32)


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
def train_svm(training_data, labels_x, labels_y):
    try:
        # Treinar SVM para coordenada x
        svm_x = cv2.ml.SVM_create()
        svm_x.setType(cv2.ml.SVM_EPS_SVR)
        svm_x.setKernel(cv2.ml.SVM_LINEAR)
        svm_x.setP(0.1)  # Definindo epsilon
        svm_x.setTermCriteria((cv2.TERM_CRITERIA_MAX_ITER, 100, 1e-6))
        svm_x.train(training_data, cv2.ml.ROW_SAMPLE, labels_x)
        
        # Treinar SVM para coordenada y
        svm_y = cv2.ml.SVM_create()
        svm_y.setType(cv2.ml.SVM_EPS_SVR)
        svm_y.setKernel(cv2.ml.SVM_LINEAR)
        svm_y.setP(0.1)  # Definindo epsilon
        svm_y.setTermCriteria((cv2.TERM_CRITERIA_MAX_ITER, 100, 1e-6))
        svm_y.train(training_data, cv2.ml.ROW_SAMPLE, labels_y)
        
        return svm_x, svm_y
    except ValueError as e:
        if "setting an array element with a sequence" in str(e):
            print(f"Erro ao treinar o modelo SVM. Detalhes: {e}")
            return None, None
        else:
            raise e

def check_and_normalize_data(training_data, labels_x, labels_y):
    # Verificando a forma
    print("Forma de training_data:", training_data.shape)
    print("Forma de labels_x:", labels_x.shape)
    print("Forma de labels_y:", labels_y.shape)

    # Verificando NaN e infinitos
    print("NaN em training_data:", np.isnan(training_data).sum())
    print("Infinitos em training_data:", np.isinf(training_data).sum())
    print("NaN em labels_x:", np.isnan(labels_x).sum())
    print("Infinitos em labels_x:", np.isinf(labels_x).sum())
    print("NaN em labels_y:", np.isnan(labels_y).sum())
    print("Infinitos em labels_y:", np.isinf(labels_y).sum())

    # Verificar a necessidade de normalização usando a diferença entre o valor máximo e mínimo
    print("Normalizando os dados...")
    mean = training_data.mean(axis=0)
    std = training_data.std(axis=0)
    
    # Evitar divisão por zero
    std = np.where(std == 0, 1, std)
    
    training_data_normalized = (training_data - mean) / std

    return training_data_normalized, labels_x, labels_y



def save_and_show_image_with_detections(image_path, image, svm_coords, dlib_coords, save_dir="resultado_SVM"):
    plt.figure(figsize=(10, 10))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))  # Convertendo a imagem de BGR para RGB
    plt.scatter([svm_coords[0]], [svm_coords[1]], color='r', s=100, label='SVM Detection')  # Vermelho para detecção SVM

    # Dlib retorna vários pontos em torno da boca. Portanto, vamos pegar a média para ter um único ponto central.
    if dlib_coords:
        mean_dlib_coords = (sum(p.x for p in dlib_coords) / len(dlib_coords),
                            sum(p.y for p in dlib_coords) / len(dlib_coords))
        plt.scatter([mean_dlib_coords[0]], [mean_dlib_coords[1]], color='g', s=100, label='Dlib Detection')  # Verde para detecção Dlib

    plt.legend()

    # Verificar se o diretório de salvamento existe, senão, criar.
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Montar o caminho completo para salvar a imagem
    save_path = os.path.join(save_dir, os.path.basename(image_path))
    plt.savefig(save_path)

    plt.show()  # Adicionado para exibir a imagem plotada
    plt.close()
##############################################################################################################################################################################

def main():
    detector = FaceDetector()

    # Load and train
    images, contours = load_data("pre_imagem_label", "anotacao")
    if not images:
        print("Lista de imagens está vazia.")
    if not contours:
        print("Lista de contornos está vazia.")
    if not images or not contours:
        print("Não foi possível carregar as imagens ou anotações. Encerrando.")
        return
   
    training_data, labels_x, labels_y = extract_features(images, contours, detector)
    
    # Verifique se o número de amostras em training_data é igual ao número de rótulos em labels_x e labels_y.
    assert training_data.shape[0] == labels_x.shape[0] == labels_y.shape[0], "Inconsistência nos tamanhos de dados e rótulos!"
    
    # Verificação adicional
    if not training_data.size:
        print("Sem dados de treinamento válidos. Encerrando.")
        return
    
    # Check and normalize data
    training_data, labels_x, labels_y = check_and_normalize_data(training_data, labels_x, labels_y)
    
    svm_x, svm_y = train_svm(training_data, labels_x, labels_y)

    if svm_x is None or svm_y is None:
        print("Erro ao treinar o SVM. Encerrando.")
        return
    
    # Process test images
    test_image_dir  = "diretoria_pprocessado"
    image_files = [f for f in os.listdir(test_image_dir) if os.path.isfile(os.path.join(test_image_dir, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    for image_file in image_files:
        image_file_path = os.path.join(test_image_dir, image_file)

        if os.path.exists(image_file_path):
            test_image = cv2.imread(image_file_path)
            if test_image is not None:
                # Adicionando logs
                print(f"Processando a imagem: {image_file_path}")
                x_pred, y_pred = detector.svm_detection(test_image, svm_x, svm_y)
                print(f"Para a imagem {image_file}:")
                print("SVM Detection para x:", x_pred)
                print("SVM Detection para y:", y_pred)
                dlib_results = detector.dlib_detection(test_image)
                if dlib_results:
                    print("Dlib Mouth Coords:", dlib_results)
                    save_and_show_image_with_detections(image_file_path, test_image, (x_pred, y_pred), dlib_results[0])
                else:
                    print("Dlib não detectou marcos faciais para esta imagem.")
            else:
                print(f"Erro ao carregar a imagem de teste: {image_file_path}")
        else:
            print(f"Erro: {image_file_path} não existe!")
    
    
if __name__ == '__main__':
    main()
