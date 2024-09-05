import cv2
import numpy as np
from PIL import Image

def rgb_to_yiq(r, g, b):
    y = r*0.299 + g*0.587 + b*0.114
    i = r*0.596 - g*0.274 - b*0.322
    q = r*0.211 - g*0.523 - b*0.312
    
    return y, i, q

def yiq_to_rgb(yiq):
    r = yiq[0] + yiq[1]*0.956 + yiq[2]*0.621
    g = yiq[0] - yiq[1]*0.272 - yiq[2]*0.647
    b = yiq[0] - yiq[1]*1.106 + yiq[2]*1.703
    
    if r < 0:
        r  = 0

    elif r > 255:
        r = 255

    if g < 0:
        g  = 0
        
    elif g > 255:
        g = 255
    
    if b < 0:
        b  = 0
        
    elif b > 255:
        b = 255

    return round(r), round(g), round(b)

#Carrega a imagem
# imagem = cv2.imread('imagens/arara_dis.jpeg')
imagem = cv2.imread('imagens/Shapes.png')
# imagem = cv2.imread('imagens/testpat.1k.color2.tif')

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

yiq = []
new_rgb = []

#Inicializando a matriz que guardara o novos valores de R G B da imagem
new_matriz = matriz_imagem

#Loop que fará o filtro percorrer toda a imagem
for x in range(altura): 
    for j in range(largura):
        yiq = rgb_to_yiq(r[x][j], g[x][j], b[x][j])

        #Alterando valor do canal Y
        if yiq[0] > 0 and yiq[0] <= 128:
            new_y = 2 * yiq[0]
            if new_y > 255:
                new_y = 255
        
        elif yiq[0] > 128 and yiq[0] < 255:
            new_y = yiq[0]/2

        else:
            new_y = 0
        
        new_rgb = yiq_to_rgb(yiq)

        #Atribui os novos valores ao canais
        new_matriz[x][j] = int(new_rgb[0]) , int(new_rgb[1]), int(new_rgb[2])

#Criando a imagem filtrada a partir da matriz 
new_imagem = Image.fromarray(new_matriz)
# new_imagem.save('imagens_filtradas/arara_pontual.jpeg')
new_imagem.save('imagens_filtradas/Shapes_pontual_YIQ.png')
# new_imagem.save('imagens_filtradas/testpat.1k.color2_pontual.tif')