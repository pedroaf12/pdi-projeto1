import numpy as np
from PIL import Image
import cv2

image_path = 'images/arara.jpeg'
filtro_path = 'filtros/filtro-sobel-horizontal.txt'
output_image_name = 'output/image-correletion-sobel-horiz.png'

# m = linhas
# n = colunas

def read_filter_file(file):
    filtro = []
    with open(file, 'r') as arq:
        linha = arq.readline().strip().split(',')
        m, n, offset = int(linha[0]), int(linha[1]), int(linha[2])

        for l in range(m):
            l = arq.readline().strip().split(',')
            for k in range(n):
                filtro.append(l[k])

    return m,n, offset, filtro

    
def valor_absoluto(pixel):
    if pixel < 0:
        pixel = pixel*(-1)
    return pixel

def rgb_para_yiq(image):
    imagem = cv2.imread(image)

    if imagem is None:
        print("Erro na leitura da imagem")
        return 0
    
    height, width, canais = imagem.shape
    img_matriz = imagem

    print(f"Imagem original {height}x{width}")
                                                                   
    b,g,r = cv2.split(img_matriz) 


    for x in range(height):
        for z in range(width):

            y = (r[x, z]*0.299) + (g[x, z]*0.587) + (b[x, z]*0.114)
            i = (r[x, z]*0.596) - (g[x, z]*0.274) - (b[x, z]*0.322)
            q = (r[x, z]*0.211) - (g[x, z]*0.523) + (b[x, z]*0.312)

            # pixel_r = (y) + (i*0.956) + (q*0.621)
            # pixel_g = (y) - (i*0.272) - (q*0.647)
            # pixel_b = (y) - (i*1.106) + (q*1.703)

            img_matriz[x][z] = y, i, q
    

    filtered_image = Image.fromarray(img_matriz)
    filtered_image.save(output_image_name)
    height, width, canais= img_matriz.shape
    print(f"Imagem com correlacao {height}x{width}")



def transform(matriz, m, n):
    rows, cols = matriz.shape
    matriz_res = np.zeros((m,n))
    matriz_res[:rows, :cols] = matriz

    return matriz_res


def correlacao(image, m, n, filtro):
    imagem = cv2.imread(image)

    if imagem is None:
        print("Erro na leitura da imagem")
        return 0
    
    height, width, canais = imagem.shape
    img_matriz = imagem

    print(f"Imagem original {height}x{width}")
                                                                   
    b,g,r = cv2.split(img_matriz)                              
    matriz_aux = np.zeros((m,n), dtype=float)
    
    for x in range(height):
        for y in range(width):
            r_padded = transform(r[x:x+m, y:y+n], m, n)
            matriz_aux[:,:] = r_padded
            matriz_aux =  matriz_aux * filtro
            pixel_r = (np.sum(matriz_aux))
            # pixel_r = pixel_r + offset
            pixel_r = valor_absoluto(pixel_r)

            g_padded = transform(g[x:x+m, y:y+n], m, n)
            matriz_aux[:,:] = g_padded
            matriz_aux = matriz_aux * filtro
            pixel_g = (np.sum(matriz_aux))
            # pixel_g = pixel_g + offset
            pixel_g = valor_absoluto(pixel_g)
            

            b_padded = transform(b[x:x+m, y:y+n], m, n)
            matriz_aux[:,:] = b_padded
            matriz_aux = matriz_aux * filtro
            pixel_b = (np.sum(matriz_aux))
            # pixel_b = pixel_b + offset
            pixel_b = valor_absoluto(pixel_b)

            img_matriz[x][y] = pixel_r, pixel_g, pixel_b
            
            
        
    filtered_image = Image.fromarray(img_matriz)
    filtered_image.save(output_image_name)
    height, width, canais = img_matriz.shape
    print(f"Imagem com correlacao {height}x{width}")
    
    
    

m,n,offset, filtro = read_filter_file(filtro_path)

# rgb_para_yiq(image_path)



matriz = np.array(filtro)
matriz = matriz.reshape(m,n)
matriz = matriz.astype(float)
correlacao(image_path, m,n, matriz)


