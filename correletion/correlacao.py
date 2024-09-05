import cv2
import numpy as np
from PIL import Image

#Carrega a imagem
imagem = cv2.imread('imagens/arara_dis.jpeg')

def transform(matriz, m, n):
    rows, cols = matriz.shape
    matriz_res = np.zeros((m,n))
    matriz_res[:rows, :cols] = matriz

    return matriz_res

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

#Lendo arquivo da mascara do filtro
counter_line = 0

with open('filtro.txt', 'r') as file:
    if counter_line == 0:
        linha = file.readline().strip().split(',')
        num_linhas = int(linha[0])
        num_colunas = int(linha[1])
        offset = float(linha[2])
        counter_line += 1

    #Criando a matriz da mascara apartir de m x n definidos no arquivo 
    mascara = np.zeros((num_linhas, num_colunas), dtype=float)
    #print(mascara)
    
    linha = file.readline().strip()
    i=0
    #Colocando enfim os valores da mascara do filtro na matriz
    while linha:
        mascara[i:, 0:num_colunas] = linha.split(',')
        counter_line += 1
        linha = file.readline().strip()
        i= i+1

print(np.sum(mascara))
#Inicializando a matriz que guardara o novos valores de R G B da imagem
new_matriz = matriz_imagem

#Criando matriz auxiliar para ajudar nas operações
matriz_aux = np.zeros((num_linhas, num_colunas), dtype=float)
#print(matriz_aux)

#Loop que fará o filtro percorrer toda a imagem
for x in range(altura): 
    for y in range(largura):

        #Coletando valores do canal R para a matriz auxiliar
        matriz_aux = transform(r[x:x+num_colunas, y:y+num_linhas], num_linhas, num_colunas)

        #Realizando a correlação 
        matriz_aux = matriz_aux * mascara
        soma_r = (np.sum(matriz_aux))#/np.sum(mascara)
        soma_r = soma_r + offset
        
        if soma_r > 255:
            soma_r = 255
        elif soma_r < 0:
            soma_r = 0
        #Coletando valores do canal G para a matriz auxiliar
        matriz_aux = transform(g[x:x+num_colunas, y:y+num_linhas], num_linhas, num_colunas)

        #Realizando a correlação 
        matriz_aux = matriz_aux * mascara
        soma_g = (np.sum(matriz_aux))#/np.sum(mascara)
        soma_g = soma_g + offset
        
        if soma_g > 255:
            soma_g = 255

        elif soma_g < 0:
            soma_g = 0
        #Coletando valores do canal B para a matriz auxiliar
        matriz_aux = transform(b[x:x+num_colunas, y:y+num_linhas], num_linhas, num_colunas)
    
        #Realizando a correlação 
        matriz_aux = matriz_aux * mascara
        soma_b = (np.sum(matriz_aux))#/np.sum(mascara)
        soma_b = soma_b + offset
        
        if soma_b > 255:
            soma_b = 255
        
        elif soma_b < 0:
            soma_b = 0
            
        #Atribui os novos valores ao canais
        new_matriz[x][y] = int(soma_r) , int(soma_g), int(soma_b)
            
#Criando a imagem filtrada a partir da matriz 
new_imagem = Image.fromarray(new_matriz)
new_imagem.save('imagens_filtradas/arara_filtrada.jpeg')

