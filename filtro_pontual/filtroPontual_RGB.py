import cv2
import numpy as np
from PIL import Image

#Carrega a imagem
imagem = cv2.imread('imagens/arara_dis.jpeg')
#imagem = cv2.imread('imagens/Shapes.png')
#imagem = cv2.imread('imagens/testpat.1k.color2.tif')

#Verifica se a imagem foi carregada corretamente
if imagem is None:
    print('Erro ao carregar a imagem')
else:
    # Exibe as dimensões da imagem
    altura, largura, canais = imagem.shape
    print('Dimensões da imagem:', altura, 'x', largura)

    # Converte a imagem para uma matriz numpy
    matriz_imagem = imagem

#Separando a imagem em matrizes por canal de cor
b, g , r = cv2.split(matriz_imagem)

#Inicializando a matriz que guardara o novos valores de R G B da imagem
new_matriz = matriz_imagem

#Loop que fará o filtro percorrer toda a imagem
for x in range(altura): 
    for y in range(largura):

        #Alterando valor do canal R
        if r[x][y] > 0 and r[x][y] <= 128:
            new_r = 2 * r[x][y]
            if new_r > 255:
                new_r = 255
        
        elif r[x][y] > 128 and r[x][y] < 255:
            new_r = r[x][y]/2

        else:
            new_r = 0
        
        #Alterando valor do canal G
        if g[x][y] > 0 and g[x][y] <= 128:
            new_g = 2 * g[x][y]
            if new_g > 255:
                new_g = 255

        elif g[x][y] > 128 and g[x][y] < 255:
            new_g = g[x][y]/2

        else:
            new_g = 0

        #Alterando valor do canal B
        if b[x][y] > 0 and b[x][y] <= 128:
            new_b = 2 * b[x][y]
            if new_b > 255:
                new_b = 255
        
        elif b[x][y] > 128 and b[x][y] < 255:
            new_b = b[x][y]/2

        else:
            new_b = 0

        #Atribui os novos valores ao canais
        new_matriz[x][y] = int(new_r) , int(new_g), int(new_b)

#Criando a imagem filtrada a partir da matriz 
new_imagem = Image.fromarray(new_matriz)
new_imagem.save('imagens_filtradas/arara_pontual.jpeg')
# new_imagem.save('imagens_filtradas/Shapes_pontual.png')
#new_imagem.save('imagens_filtradas/testpat.1k.color2_pontual.tif')