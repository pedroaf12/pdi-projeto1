import numpy as np
from PIL import Image
import cv2

image_path = 'images/Shapes.png'
output_image_name = 'output/shapes-filter.png'

def define_equacao_da_reta():
    #Calcula inclinação m
    m = (0-255)/(255-128)

    #Calcula coeficiente linear b
    b = 255 - (m*128)

    return m, b

def pixel_maior_que_128(pixel, m, b):
    y = m*pixel + b
    return y

def pixel_menor_igual_128(pixel):
    y = (pixel*255)/128
    return y

m, n = define_equacao_da_reta() # Armazena os valores da reta de descida do filtro pontual
print(m, n)

imagem = cv2.imread(image_path)
if imagem is None:
    print("Erro na leitura da imagem")
    exit(0)

height, width, canais = imagem.shape
img_matriz = imagem

print(f"Imagem original {height}x{width}")

b,g,r = cv2.split(img_matriz)

for x in range(height):
    for y in range(width):
        if r[x][y] <= 128:
            pixel_r = pixel_menor_igual_128(int(r[x][y]))
        else:
            pixel_r = pixel_maior_que_128(int(r[x][y]), m, n)
        
        if g[x][y] <= 128:
            pixel_g = pixel_menor_igual_128(int(g[x][y]))
        else:
            pixel_g = pixel_maior_que_128(int(g[x][y]), m, n)
        
        if b[x][y] <= 128:
            pixel_b = pixel_menor_igual_128(int(b[x][y]))
        else:
            pixel_b = pixel_maior_que_128(int(b[x][y]), m, n)
        
        img_matriz[x][y] = pixel_r, pixel_g, pixel_b

filtered_image = Image.fromarray(img_matriz)
filtered_image.save(output_image_name)