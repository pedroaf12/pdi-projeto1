import numpy as np
from PIL import Image
import cv2

image_path = 'images/arara.jpeg'
output_image_name = 'output/arara-filter2.jpeg'

def rgb_to_yiq(rgb):
    r,g,b = rgb[0], rgb[1], rgb[2]

    y = (0.299*r + 0.587*g + 0.114*b)
    i = (0.596*r - 0.275*g - 0.321*b)
    q = (0.212*r - 0.523*g + 0.311*b)

    return y, i, q

def yiq_to_rgb(yiq):
    y, i, q = yiq[0], yiq[1], yiq[2]

    r = 1*y + 0.956*i + 0.621*q
    g = 1*y - 0.272*i - 0.647*q
    b = 1*y - 1.106*i + 1.703*q

    return round(r), round(g), round(b)

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
        yiq = rgb_to_yiq([int(r[x][y]), int(g[x][y]), int(b[x][y])])

        if yiq[0] <= 128:
            pixel_y = pixel_menor_igual_128(int(yiq[0]))
        else:
            pixel_y = pixel_maior_que_128(int(yiq[0]), m, n)

        rgb = yiq_to_rgb([pixel_y, yiq[1], yiq[2]])
        r_aux, g_aux, b_aux = rgb[0], rgb[1], rgb[2]

        if r_aux < 0:
            r_aux = 0
        elif r_aux > 255:
            r_aux = 255
        
        if g_aux < 0:
            g_aux = 0
        elif g_aux > 255:
            g_aux = 255

        if b_aux < 0:
            b_aux = 0
        elif b_aux > 255:
            b_aux = 255
            
        img_matriz[x][y] = r_aux,g_aux,b_aux

filtered_image = Image.fromarray(img_matriz)
filtered_image.save(output_image_name)