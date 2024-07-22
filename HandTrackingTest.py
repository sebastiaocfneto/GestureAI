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

ponta_dedos = {'polegar': 4,
               'indicador': 8,
               'medio': 12,
               'anelar': 16,
               'minimo': 20
               }
# formato: dedos_levantados, dedos_a_analisar, distancia_ponta_centro_x, distancia_ponta_centro_y, movimento_x, movimento_y
#positivo: direita, cima
letras = {
    'A': [[0, 0, 0, 0, 0], 'polegar', 10, 20, 0, 0],
    'B': [[0, 1, 1, 1, 1], 'polegar', 10, 10, 0, 0],
    'C': [[1, 1, 1, 1, 1], 'medio', 10, 10, 0, 0],
    'Ç': [[1, 1, 1, 1, 1], 'medio', 10, 10, 10, 10],
    'D': [[1, 1, 0, 0, 0], 'medio', 5, 5, 0, 0],
    'E': [[0, 0, 0, 0, 0], 'medio', 0, 10, 0, 0],
    'F': [[1, 1, 1, 1, 1], 'indicador', 10, 10, 0, 0],
    'G': [[0, 1, 0, 0, 0], 'indicador', 0, 50, 0, 0],
    'H': [[1, 1, 1, 0, 0], 'medio', 30, 5, 15, 0],
    'I': [[0, 0, 0, 0, 1], 'minimo', 0, 0, 0, 0, 0],
    'J': [[0, 0, 0, 0, 1], 'minimo', 0, 0, 0, 10],
    'K': [[1, 1, 1, 0, 0], 'medio', 50, 10, 0, 5],
    'L': [[1, 1, 0, 0, 0], 'polegar', 140, 10, 0, 0],
    'M': [[0, 1, 1, 1, 0], 'medio', 0, -50, 0, 0],
    'N': [[0, 1, 1, 0, 0], 'medio', 0, -20, 0, 0],
    'O': [[1, 1, 1, 1, 1], 'polegar', 60, 20, 0, 0],
    'P': [[1, 1, 1, 0, 0], 'medio', -50, -10, 0, 0],
    'Q': [[0, 1, 0, 0, 0], 'indicador', 0, -50, 0, 0],
    'R': [[0, 1, 1, 0, 0], 'indicador', -10, 50, 0, 0],
    'S': [[0, 0, 0, 0, 0], 'polegar', 0, 0, 0, 0],
    'T': [[1, 1, 1, 1, 1], 'indicador', 10, 10, 0, 0],
    'U': [[0, 1, 1, 0, 0], 'medio', 0, 0, 0, 0],
    'V': [[0, 1, 1, 0, 0], 'medio', 20, 0, 0, 0],
    'X': [[0, 1, 0, 0, 0], 'indicador', -20, 0, -20, 0],
    'W': [[0, 1, 1, 1, 0], 'polegar', 0, 0, 0, 50],
    'Y': [[1, 0, 0, 0, 1], 'minimo', 0, 50, 40, 0],
    'Z': [[0, 1, 0, 0, 0], 'indicador', 0, 50, -10, -10]

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
    if hands:
        previous_position = {
            'polegar': hands[0]['lmList'][ponta_dedos['polegar']],
            'indicador': hands[0]['lmList'][ponta_dedos['indicador']],
            'medio': hands[0]['lmList'][ponta_dedos['medio']],
            'anelar': hands[0]['lmList'][ponta_dedos['anelar']],
            'minimo': hands[0]['lmList'][ponta_dedos['minimo']],

        }

        for letra, valor in letras.items():
            hand = hands[0]

            if len(hand['lmList']) > 0:  # Certifica-se de que há landmarks detectados
                point = hand['lmList'][ponta_dedos[valor[1]]]
                center = hand['center']
                distX = calcDistX(point, center)
                distY = calcDistY(point, center)
                mov_x = calcDistX(point, previous_position[valor[1]])
                mov_y = calcDistY(point, previous_position[valor[1]])
                fingers = detector.fingersUp(hand)
                if fingers == valor[0] and distX >= valor[2] and distY >= valor[3] and mov_x >= valor[4] and mov_y >= valor[5]:
                    print(f"Letra detectada: {letra}")

                    img1 = cv2.imread(f'alfabeto/{letra.lower()}.png')
                    h1, w1, _ = img1.shape
                    newH, newW = (h1 + 50 // 2) * 2, (w1 + 50 // 2) * 2
                    img1 = cv2.resize(img1, (newW, newH))
                    img1 = cv2.flip(img1, 1)
                    img[256:544, 240:488] = img1

    # espelhando a imagem horizontalmente para melhor localização
    img = cv2.flip(img, 1)

    cv2.imshow("Image", img)
    # caso a tecla 'q' seja pressionada, o loop encerra
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
