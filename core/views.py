from django.http import StreamingHttpResponse
from django.shortcuts import render
import cv2
import numpy as np
import threading


def home(request):
    return render(request, 'home/home.html')

def index(request):
    return render(request, 'index.html')

# Cámara
# Cambiar el 1 por el numero donde se encuentre su camara
cap = cv2.VideoCapture(0)

# Configuración del color
celesteBajo = np.array([75, 185, 88], np.uint8)
celesteAlto = np.array([112, 255, 255], np.uint8)
colorCeleste = (255,113,82)
colorAmarillo = (89,222,255)
colorRosa = (128,0,255)
colorVerde = (0,255,36)
colorLimpiarPantalla = (29,112,246)
comando_voz = {"valor": None}

grosorCeleste, grosorAmarillo, grosorRosa, grosorVerde = 6,2,2,2
grosorPeque, grosorMedio, grosorGrande = 6,1,1
color = colorCeleste
grosor = 3
x1, y1, imAux = None, None, None

lock = threading.Lock()  # Para sincronizar imAux entre hilos

# --- Función que actualiza continuamente imAux ---
def update_frame():
    global x1, y1, imAux, color, grosor
    global grosorCeleste, grosorAmarillo, grosorRosa, grosorVerde
    global grosorPeque, grosorMedio, grosorGrande
    global comando_voz

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame,1)
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        if imAux is None:
            imAux = np.zeros(frame.shape, dtype=np.uint8)

        # --- Dibujar botones ---
        cv2.rectangle(frame,(0,0),(50,50),colorAmarillo,grosorAmarillo)
        cv2.rectangle(frame,(50,0),(100,50),colorRosa,grosorRosa)
        cv2.rectangle(frame,(100,0),(150,50),colorVerde,grosorVerde)
        cv2.rectangle(frame,(150,0),(200,50),colorCeleste,grosorCeleste)
        cv2.rectangle(frame,(300,0),(400,50),colorLimpiarPantalla,1)
        cv2.putText(frame,'Limpiar',(320,20),6,0.6,colorLimpiarPantalla,1,cv2.LINE_AA)
        cv2.putText(frame,'pantalla',(320,40),6,0.6,colorLimpiarPantalla,1,cv2.LINE_AA)
        cv2.rectangle(frame,(490,0),(540,50),(0,0,0),grosorPeque)
        cv2.circle(frame,(515,25),3,(0,0,0),-1)
        cv2.rectangle(frame,(540,0),(590,50),(0,0,0),grosorMedio)
        cv2.circle(frame,(565,25),7,(0,0,0),-1)
        cv2.rectangle(frame,(590,0),(640,50),(0,0,0),grosorGrande)
        cv2.circle(frame,(615,25),11,(0,0,0),-1)

        # --- Detectar marcador celeste ---
        maskCeleste = cv2.inRange(frameHSV, celesteBajo, celesteAlto)
        maskCeleste = cv2.erode(maskCeleste,None,iterations=1)
        maskCeleste = cv2.dilate(maskCeleste,None,iterations=2)
        maskCeleste = cv2.medianBlur(maskCeleste,13)
        cnts,_ = cv2.findContours(maskCeleste, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:1]

        for c in cnts:
            area = cv2.contourArea(c)
            if area > 1000:
                x,y,w,h = cv2.boundingRect(c)
                x2, y2 = x+w//2, y+h//2

                # Cambiar color
                if 0 < x2 < 50 and 0 < y2 < 50:
                    color = colorAmarillo
                    grosorAmarillo, grosorRosa, grosorVerde, grosorCeleste = 6,2,2,2
                if 50 < x2 < 100 and 0 < y2 < 50:
                    color = colorRosa
                    grosorAmarillo, grosorRosa, grosorVerde, grosorCeleste = 2,6,2,2
                if 100 < x2 < 150 and 0 < y2 < 50:
                    color = colorVerde
                    grosorAmarillo, grosorRosa, grosorVerde, grosorCeleste = 2,2,6,2
                if 150 < x2 < 200 and 0 < y2 < 50:
                    color = colorCeleste
                    grosorAmarillo, grosorRosa, grosorVerde, grosorCeleste = 2,2,2,6

                # Cambiar grosor
                if 490 < x2 < 540 and 0 < y2 < 50:
                    grosor = 3
                    grosorPeque, grosorMedio, grosorGrande = 6,1,1
                if 540 < x2 < 590 and 0 < y2 < 50:
                    grosor = 7
                    grosorPeque, grosorMedio, grosorGrande = 1,6,1
                if 590 < x2 < 640 and 0 < y2 < 50:
                    grosor = 11
                    grosorPeque, grosorMedio, grosorGrande = 1,1,6

                # Limpiar lienzo
                if 300 < x2 < 400 and 0 < y2 < 50:
                    with lock:
                        imAux = np.zeros(frame.shape, dtype=np.uint8)

                # Dibujar
                if x1 is not None and y1 is not None and not (0<y2<60):
                    with lock:
                        imAux = cv2.line(imAux,(x1,y1),(x2,y2),color,grosor)

                x1, y1 = x2, y2
            else:
                x1, y1 = None, None
        
        if comando_voz["valor"]:
            if "amarillo" in comando_voz["valor"]:
                color = colorAmarillo
                grosorAmarillo, grosorRosa, grosorVerde, grosorCeleste = 6,2,2,2
            elif "rosa" in comando_voz["valor"]:
                color = colorRosa
                grosorAmarillo, grosorRosa, grosorVerde, grosorCeleste = 2,6,2,2
            elif "verde" in comando_voz["valor"]:
                color = colorVerde
                grosorAmarillo, grosorRosa, grosorVerde, grosorCeleste = 2,2,6,2
            elif "celeste" in comando_voz["valor"]:
                color = colorCeleste
                grosorAmarillo, grosorRosa, grosorVerde, grosorCeleste = 2,2,2,6
            comando_voz["valor"] = None
        
        
        # --- Guardar última cámara para stream ---
        with lock:
            frame_copy = frame.copy()
        global last_frame_cam
        last_frame_cam = frame_copy

# Arrancar el hilo de actualización
threading.Thread(target=update_frame, daemon=True).start()

# --- Stream de cámara ---
def video_feed_cam(request):
    def gen():
        global last_frame_cam
        import time
        while True:
            if 'last_frame_cam' not in globals(): 
                time.sleep(0.01)
                continue
            with lock:
                frame = last_frame_cam.copy()
            ret, jpeg = cv2.imencode('.jpg', frame)
            if not ret: continue
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
    return StreamingHttpResponse(gen(), content_type='multipart/x-mixed-replace; boundary=frame')

# --- Stream del lienzo ---
def video_feed_canvas(request):
    def gen():
        global imAux
        import time
        while True:
            if imAux is None:
                time.sleep(0.01)
                continue
            with lock:
                canvas = imAux.copy()
            ret, jpeg = cv2.imencode('.jpg', canvas)
            if not ret: continue
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
    return StreamingHttpResponse(gen(), content_type='multipart/x-mixed-replace; boundary=frame')
