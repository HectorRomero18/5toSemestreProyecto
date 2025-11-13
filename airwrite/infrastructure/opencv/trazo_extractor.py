import cv2
import numpy as np
import random
from airwrite.domain.services.generar_modelo_texto import generar_modelo_texto
from airwrite.domain.services.generar_lista import generar_lista
from airwrite.domain.services.evaluar_trazo import evaluar_trazo_por_contorno

# Colores y parámetros
celesteBajo = np.array([75, 185, 88], np.uint8)
celesteAlto = np.array([112, 255, 255], np.uint8)
colorDibujo = (255, 113, 82)
colorPuntero = (255, 0, 0)
fondo_color = (0, 255, 255)
BAND_DILATE = 15
STROKE_DILATE = 8

def reiniciar_lienzo(frame_shape, texto):
    """Crea el lienzo y el modelo base de la letra/sílaba/numero."""
    h, w = frame_shape[:2]
    modelo = generar_modelo_texto((h, w), texto)
    letra_bgr = cv2.cvtColor(modelo, cv2.COLOR_GRAY2BGR)
    fondo = np.full((h, w, 3), fondo_color, dtype=np.uint8)
    base = cv2.addWeighted(fondo, 1.0, letra_bgr, 0.95, 0)
    return base.copy(), modelo

def iniciar_practica(modo="letras"):
    """Inicia el flujo de práctica (con cámara y reconocimiento del trazo)."""
    elementos = generar_lista(modo)
    random.shuffle(elementos)

    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    if not cap.isOpened():
        raise RuntimeError("No se pudo abrir la cámara")

    ret, frame = cap.read()
    if not ret:
        raise RuntimeError("No se pudo leer la cámara")

    frame = cv2.flip(frame, 1)
    indice = 0
    elemento_actual = elementos[indice]
    base_canvas, modelo_gray = reiniciar_lienzo(frame.shape, elemento_actual)
    imAux = base_canvas.copy()

    grosor = 28
    dibujando = False
    x1 = y1 = None

    print("\nControles: [A] dibujar/pause | [E] evaluar | [ESP] limpiar | [←][→] siguiente/anterior | [ESC] salir")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, celesteBajo, celesteAlto)
        mask = cv2.erode(mask, None, iterations=1)
        mask = cv2.dilate(mask, None, iterations=2)
        mask = cv2.medianBlur(mask, 7)
        cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        cursor = None
        if cnts:
            c = max(cnts, key=cv2.contourArea)
            if cv2.contourArea(c) > 800:
                x, y, w, h = cv2.boundingRect(c)
                cx = x + w // 2
                cy = y + h // 2
                cursor = (cx, cy)
                if dibujando:
                    if x1 is not None:
                        cv2.line(imAux, (x1, y1), (cx, cy), colorDibujo, grosor, cv2.LINE_AA)
                    x1, y1 = cx, cy
                else:
                    x1, y1 = cx, cy
        else:
            x1, y1 = None, None

        view = imAux.copy()
        if cursor:
            cv2.circle(view, cursor, 10, colorPuntero, -1)

        cv2.imshow("Camara", frame)
        cv2.imshow(f"Lienzo - {elemento_actual}", view)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC
            break
        elif key in (ord('a'), ord('A')):
            dibujando = not dibujando
        elif key == 32:
            base_canvas, modelo_gray = reiniciar_lienzo(frame.shape, elemento_actual)
            imAux = base_canvas.copy()
        elif key in (ord('e'), ord('E')):
            score, overlay = evaluar_trazo_por_contorno(imAux, base_canvas, modelo_gray,
                                                         band_dilate=BAND_DILATE,
                                                         stroke_dilate=STROKE_DILATE)
            print(f"Precisión: {score:.2f}%")
            cv2.imshow("Evaluación", overlay)
            cv2.waitKey(800)
            cv2.destroyWindow("Evaluación")
            if score >= 95:
                indice = (indice + 1) % len(elementos)
                elemento_actual = elementos[indice]
                base_canvas, modelo_gray = reiniciar_lienzo(frame.shape, elemento_actual)
                imAux = base_canvas.copy()
        elif key == 81:
            indice = (indice - 1) % len(elementos)
            elemento_actual = elementos[indice]
            base_canvas, modelo_gray = reiniciar_lienzo(frame.shape, elemento_actual)
            imAux = base_canvas.copy()
        elif key == 83:
            indice = (indice + 1) % len(elementos)
            elemento_actual = elementos[indice]
            base_canvas, modelo_gray = reiniciar_lienzo(frame.shape, elemento_actual)
            imAux = base_canvas.copy()

    cap.release()
    cv2.destroyAllWindows()
