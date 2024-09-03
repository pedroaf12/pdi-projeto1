import cv2
import numpy as np

# Carregar a imagem em escala de cinza
imagem = cv2.imread('./images/frutas.png')

# Aplicar o filtro de Gauss
# ksize: tamanho do kernel (deve ser ímpar)
# sigmaX: desvio padrão no eixo X (0 deixa o OpenCV calcular com base no kernel)
imagem_suavizada = cv2.GaussianBlur(imagem, (5, 5), 0)

# Exibir a imagem original e o resultado suavizado
cv2.imshow('Imagem Original', imagem)
cv2.imshow('Imagem Suavizada', imagem_suavizada)

cv2.waitKey(0)
cv2.destroyAllWindows()