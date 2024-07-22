import math

import cv2
from cvzone.HandTrackingModule import HandDetector

# inicia a captura de video da webcam
cap = cv2.VideoCapture(0)
# define os tamanhos da captura
cap.set(3, 1280)
cap.set(4, 720)

# inicia o detector da mão usando o HandTrackingModule do cvzone
detector = HandDetector(detectionCon=0.7)
# variável que define a distância entre as mãos
startDist = None
# fator de escala do zoom, iniciado em 0
scale = 0
# coordenadas do inicio da imagem
cx, cy = 0, 0

dedos = {'polegar': 0,
         'indicador': 1,
         'médio': 2,
         'anelar': 3,
         'minimo': 4
         }
# formato: dedos_levantados, dedos_a_analisar, distancia_ponta_centro_x, distancia_ponta_centro_y, movimento_x, movimento_y
#positivo: direita, cima
letras = {
    'A': [[0, 0, 0, 0, 0], 'polegar', 1, 5, 0, 0],
    'B': [[0, 1, 1, 1, 1], 'polegar', 1, 1, 0, 0],
    'C': [[1, 1, 1, 1, 1], 'medio', 1, 1, 0, 0],
    'Ç': [[1, 1, 1, 1, 1], 'medio', 1, 1, 1, 1],
    'D': [[1, 1, 0, 0, 0], 'medio', 1, 1, 0, 0],
    'E': [[0, 0, 0, 0, 0], 'medio', 0, 1, 0, 0],
    'F': [[1, 1, 1, 1, 1], 'indicador', 1, 1, 0, 0],
    'G': [[0, 1, 0, 0, 0], 'indicador', 0, 5, 0, 0],
    'H': [[1, 1, 1, 0, 0], 'medio', 5, 1, 5, 0],
    'I': [[0, 0, 0, 0, 1], 'minimo', 1, 5, 0, 0, ],
    'J': [[0, 0, 0, 0, 1], 'minimo', 0, 0, 0, -5],
    'K': [[1, 1, 1, 0, 0], 'medio', 5, 1, 0, 5],
    'L': [[1, 1, 0, 0, 0], 'polegar', 5, 1, 0, 0],
    'M': [[0, 1, 1, 1, 0], 'medio', 0, -5, 0, 0],
    'N': [[0, 1, 1, 0, 0], 'medio', 0, -5, 0, 0],
    'O': [[1, 1, 1, 1, 1], 'polegar', 5, 1, 0, 0],
    'P': [[1, 1, 1, 0, 0], 'medio', -5, -1, 0, 0],
    'Q': [[0, 1, 0, 0, 0], 'indicador', 0, -5, 0, 0],
    'R': [[0, 1, 1, 0, 0], 'indicador', -1, 5, 0, 0],
    'S': [[0, 0, 0, 0, 0], 'polegar', 0, 0, 0, 0],
    'T': [[1, 1, 1, 1, 1], 'indicador', 1, 1, 0, 0],
    'U': [[0, 1, 1, 0, 0], 'medio', 0, 0, 0, 0],
    'V': [[0, 1, 1, 0, 0], 'medio', 1, 0, 0, 0],
    'X': [[0, 1, 0, 0, 0], 'indicador', -5, 0, -5, 0],
    'W': [[0, 1, 1, 1, 0], 'polegar', 0, 0, 0, 5],
    'Y': [[1, 0, 0, 0, 1], 'minimo', 0, 5, 5, 0],
    'Z': [[0, 1, 0, 0, 0], 'indicador', 0, 5, -1, -1]

}


def calcDistX(point1, point2):
    return point1[0] - point2[0]


def calcDistY(point1, point2):
    return point1[1] - point2[1]


while True:
    success, img = cap.read()

    # detecção das mãoes
    hands, img = detector.findHands(img)
    # confere se há mãos na tela
    if len(hands) >= 1:

        for letra, valor in letras.items():
            distX = calcDistX(hands[0][dedos[valor[1]]], hands[0]['center'])
            distY = calcDistY(hands[0][dedos[valor[1]]], hands[0]['center'])
            if detector.fingersUp(hands[0]) == valor[0]:
                print(letra)

    # espelhando a imagem horizontalmente para melhor localização
    img = cv2.flip(img, 1)

    cv2.imshow("Image", img)
    # caso a tecla 'q' seja pressionada, o loop encerra
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
