import cv2
import time
import requests

def detectar_marcador(frame):
    """Simula detección de marcador azul y devuelve coordenadas (x, y)"""
    # Convertimos a HSV y detectamos color azul (puedes ajustar luego)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_blue = (100, 150, 50)
    upper_blue = (140, 255, 255)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        c = max(contours, key=cv2.contourArea)
        (x, y, w, h) = cv2.boundingRect(c)
        if w * h > 300:  # evitar ruido
            return (x + w//2, y + h//2)
    return None


def iniciar_captura():
    cap = cv2.VideoCapture(0)
    last_point = None
    last_move_time = time.time()
    trace_points = []
    SEND_DELAY = 1.5  # segundos sin movimiento

    print("🎥 Iniciando cámara... Presiona 'q' para salir.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        point = detectar_marcador(frame)
        if point:
            trace_points.append(point)
            cv2.circle(frame, point, 5, (255, 0, 0), -1)  # marcador visual
            if last_point is None or abs(point[0]-last_point[0]) > 3 or abs(point[1]-last_point[1]) > 3:
                last_move_time = time.time()
                last_point = point

        # Si no se mueve por más de X segundos, enviar trazo
        if time.time() - last_move_time > SEND_DELAY and len(trace_points) > 5:
            print("🟢 Enviando trazo automáticamente...")
            payload = {
                "usuario": "John",
                "letra": "A",  # por ahora, puedes luego hacerlo dinámico
                "trazo": trace_points
            }
            print(payload)  # simula envío
            # Si ya tienes endpoint en Django:
            # requests.post("http://127.0.0.1:8000/api/validar-trazo/", json=payload)

            trace_points = []
            last_point = None

        cv2.imshow("Detección marcador", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
