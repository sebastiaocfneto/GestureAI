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

letras = {
    'B': [0, 1, 1, 1, 1],
    'G': [0, 1, 0, 0, 0],
    'I': [0, 0, 0, 0, 1],
    'L': [1, 1, 0, 0, 0],
    'U': [0, 1, 1, 0, 0]
}

while True:
    success, img = cap.read()

    # detecção das mãoes
    hands, img = detector.findHands(img)
    # confere se há mãos na tela
    if len(hands) >= 1:
        for letra, valor in letras.items():
            if detector.fingersUp(hands[0]) == valor:
                print(letra)

    # espelhando a imagem horizontalmente para melhor localização
    img = cv2.flip(img, 1)

    cv2.imshow("Image", img)
    # caso a tecla 'q' seja pressionada, o loop encerra
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
