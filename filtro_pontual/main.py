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

m, b = define_equacao_da_reta() # Armazena os valores da reta de descida do filtro pontual

pixel = 150 # Valor do pixel de exemplo
if pixel <= 128:
    valor = pixel_maior_que_128(pixel) # Faz uma regra de três simples para encontrar o valor na primeira reta.
else:
    valor = pixel_maior_que_128(pixel,m,b) # Faz o calculo baseado na equação da reta.

print(valor)