import numpy as np
from PIL import Image
import cv2

image_path = 'images/Lena-gray.png'
filtro_path = 'filtros/filtro.txt'
output_image_name = 'output/image-correletion.png'

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

            # Normalização 0,255 para filtros de borda
            #pixel_r = max(0, min(255, pixel_r))
            
            g_padded = transform(g[x:x+m, y:y+n], m, n)
            matriz_aux[:,:] = g_padded
            matriz_aux = matriz_aux * filtro
            pixel_g = (np.sum(matriz_aux)) + offset

            # Normalização 0,255 para filtros de borda
            #pixel_g = max(0, min(255, pixel_g))

            b_padded = transform(b[x:x+m, y:y+n], m, n)
            matriz_aux[:,:] = b_padded
            matriz_aux = matriz_aux * filtro
            pixel_b = (np.sum(matriz_aux)) + offset

            # Normalização 0,255 para filtros de borda
            #pixel_b = max(0, min(255, pixel_b))

            img_matriz[x][y] = pixel_r, pixel_g, pixel_b
        
    filtered_image = Image.fromarray(img_matriz)
    filtered_image.save(output_image_name)
    height, width, canais = img_matriz.shape
    
m,n,offset, filtro = read_filter_file(filtro_path)

matriz = np.array(filtro)
matriz = matriz.reshape(m,n)
matriz = matriz.astype(float)
correlacao(image_path, m,n, matriz)



