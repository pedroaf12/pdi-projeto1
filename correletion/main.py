import numpy as np
from PIL import Image
import cv2
import matplotlib.pyplot as plt

image_path = 'images/Lena-gray.png'
filtro_path = 'filtros/filtro-sobel-horizontal.txt'
output_image_name = 'output/image-correletion-abs.png'

def transform(matriz, m, n):
    rows, cols = matriz.shape
    matriz_res = np.zeros((m,n))
    matriz_res[:rows, :cols] = matriz

    return matriz_res

def read_filter_file(file):
    filtro = []
    with open(file, 'r') as arq:
        linha = arq.readline().strip().split(',')
        m, n, offset = int(linha[0]), int(linha[1]), int(linha[2])

        for i in range(m):
            l = arq.readline().strip().split(',')
            for k in range(n):
                filtro.append(l[k])

    return m,n, offset, filtro

def histograma(matrix_img, height, width):
    
    b,g,r = cv2.split(matrix_img)                              
    new_matrix_img = matrix_img
    r_max = np.max(r)
    r_min = np.min(r)
    
    g_max = np.max(g)
    g_min = np.min(g)

    b_max = np.max(b)
    b_min = np.min(b)

    l = 256

    for x in range(height):
        for y in range(width):
            pixel_r = ((r[x][y]-r_min)/(r_max-r_min))*(l-1)
            pixel_g = ((g[x][y]-g_min)/(g_max-g_min))*(l-1)
            pixel_b = ((b[x][y]-b_min)/(b_max-b_min))*(l-1)
            
            new_matrix_img[x][y] = pixel_r, pixel_g, pixel_b


    plt.subplot(1, 2, 2)
    plt.hist(new_matrix_img.flatten(), bins=256, color='red', alpha=0.7)
    plt.title('Histograma da Imagem Expandida após Sobel (Vertical)')
    plt.xlabel('Intensidade de Pixel')
    plt.ylabel('Frequência')

    plt.tight_layout()
    plt.show()

def correlacao(image, m, n, filtro):
    imagem = cv2.imread(image)

    if imagem is None:
        print("Erro na leitura da imagem")
        return 0
    
    height, width, canais = imagem.shape
    img_matriz = imagem

    print(f"Aplicando correlação do filtro: \n\n{filtro}\n\n em {image}")
                                                                   
    b,g,r = cv2.split(img_matriz)                              
    matriz_aux = np.zeros((m,n), dtype=float)
    
    for x in range(height):
        for y in range(width):
            r_padded = transform(r[x:x+m, y:y+n], m, n)
            matriz_aux[:,:] = r_padded
            matriz_aux =  matriz_aux * filtro
            pixel_r = (np.sum(matriz_aux)) + offset

            g_padded = transform(g[x:x+m, y:y+n], m, n)
            matriz_aux[:,:] = g_padded
            matriz_aux = matriz_aux * filtro
            pixel_g = (np.sum(matriz_aux)) + offset

            b_padded = transform(b[x:x+m, y:y+n], m, n)
            matriz_aux[:,:] = b_padded
            matriz_aux = matriz_aux * filtro
            pixel_b = (np.sum(matriz_aux)) + offset

            #img_matriz[x][y] = pixel_r, pixel_g, pixel_b

            #Aplicando valor absoluto para expansão de histograma
            img_matriz[x][y] = abs(pixel_r), abs(pixel_g), abs(pixel_b)
            
    #Função que realizara a expansão por histograma para o sobel
    #histograma(img_matriz, height, width)

            
    filtered_image = Image.fromarray(img_matriz)
    filtered_image.save(output_image_name)
    height, width, canais = img_matriz.shape
    
m,n,offset, filtro = read_filter_file(filtro_path)

matriz = np.array(filtro)
matriz = matriz.reshape(m,n)
matriz = matriz.astype(float)
correlacao(image_path, m,n, matriz)



