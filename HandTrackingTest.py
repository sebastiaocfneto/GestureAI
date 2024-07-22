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
    current = None
    # detecção das mãoes
    hands, img = detector.findHands(img)
    # confere se há mãos na tela
    if len(hands) >= 1:
        for letra, valor in letras.items():
            if detector.fingersUp(hands[0]) == valor:
                current = letra
                print(letra)

    # mostrando a letra como imagem

        # redefine a imagem com a nova escala
    if current:
        img1 = cv2.imread(f'alfabeto/{current.lower()}.png')
        h1, w1, _ = img1.shape
        newH, newW = (h1 + 50 // 2) * 2, (w1 + 50 // 2) * 2
        img1 = cv2.resize(img1, (newW, newH))
        img1 = cv2.flip(img1, 1)
        img[256:544, 240:488] = img1

    img = cv2.flip(img, 1)

    cv2.imshow("Image", img)
    # caso a tecla 'q' seja pressionada, o loop encerra
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
