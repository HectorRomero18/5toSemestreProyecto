from django.http import StreamingHttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import cv2
import time
import json

from django.views.decorators.http import require_POST
from airwrite.infrastructure.models.letra import Letra

from airwrite.application.use_cases.drawing_loop import DrawingLoop, DrawingConfig, DrawingState
from airwrite.infrastructure.repositories.state import OpenCVCamera, CanvasState, CommandState
from airwrite.infrastructure.repositories.adapters import CameraAdapter, CanvasAdapter, CommandAdapter

from airwrite.domain.constants.xp_reward import DIFICULTADES, CATEGORIAS_LETRAS
import unicodedata

def quitar_tildes(texto: str) -> str:
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

CATEGORIAS_DICT = dict(CATEGORIAS_LETRAS)
DIFICULTADES_DICT = dict(DIFICULTADES)


_camera = OpenCVCamera(index=0)
_canvas_state = CanvasState()
_cmd_state = CommandState()

_cam_port = CameraAdapter(_camera)
_canvas_port = CanvasAdapter(_canvas_state)
_cmd_port = CommandAdapter(_cmd_state)

_cfg = DrawingConfig(
    celeste_low=(75, 185, 88),
    celeste_high=(112, 255, 255),
    color_celeste=(255, 113, 82),
    color_amarillo=(89, 222, 255),
    color_rosa=(128, 0, 255),
    color_verde=(0, 255, 36),
    color_clear=(29, 112, 246),
    target_size=(600, 1080)
)
_state = DrawingState()
_loop = DrawingLoop(_cam_port, _canvas_port, _cmd_port, _cfg, _state)


@login_required
def index(request, letra_id=None):
    context = {
        'letra_id': letra_id,
    }
    # Usar plantilla en airwrite/templates/airwrite/index.html
    return render(request, 'airwrite/index.html', context)


def _lazy_start():
    _cam_port.start()


def video_feed_cam(request):
    def gen():
        while True:
            _lazy_start()
            _loop.step()
            frame = _loop.get_last_camera()
            if frame is None:
                time.sleep(0.01)
                continue
            ret, jpeg = cv2.imencode('.jpg', frame)
            if not ret:
                continue
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
    return StreamingHttpResponse(gen(), content_type='multipart/x-mixed-replace; boundary=frame')

def video_feed_canvas(request, letra_id=None):
    letra = get_object_or_404(Letra, id=letra_id)
    texto = DIFICULTADES_DICT.get(letra.dificultad, '')
    texto_sin_tilde = quitar_tildes(texto)

    def gen():
        while True:
            _lazy_start()
            _loop.step()
            canvas = _canvas_port.get()

            if canvas is None:
                time.sleep(0.01)
                continue

            no_bloqueadas = ["Letra A", "Letra B", "Letra C"]

            # cargar la imagen de la letra con transparencia
            if letra.bloqueada == False or letra.nombre in no_bloqueadas:
                img_path = letra.imagen.path
                letra_img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)  # RGBA

                if letra_img is None:
                    print(f"Error al leer la imagen de la letra con ID {letra.id}.")
                    continue

                # Redimensionar la letra a 500x499 píxeles
                letra_img = cv2.resize(letra_img, (500, 499), interpolation=cv2.INTER_AREA)

                # Coordenadas para centrar la letra en el lienzo
                y1 = max((canvas.shape[0] - letra_img.shape[0]) // 2, 0)
                x1 = max((canvas.shape[1] - letra_img.shape[1]) // 2, 0)
                y2 = y1 + letra_img.shape[0]
                x2 = x1 + letra_img.shape[1]

                # Ajustar si la imagen se pasa del lienzo
                y2 = min(y2, canvas.shape[0])
                x2 = min(x2, canvas.shape[1])
                letra_img = letra_img[:y2-y1, :x2-x1]

                # Mezclar imagen con transparencia si tiene canal alfa
                if letra_img.shape[2] == 4:
                    b, g, r, a = cv2.split(letra_img)
                    alpha_mask = a / 255.0
                    alpha_inv = 1.0 - alpha_mask

                    for c, channel in enumerate([b, g, r]):
                        canvas[y1:y2, x1:x2, c] = (alpha_mask * channel + alpha_inv * canvas[y1:y2, x1:x2, c])
                else:
                    canvas[y1:y2, x1:x2, :] = letra_img

                # agregar el nombre y la categoria de la letra
                cv2.putText(canvas, f"{letra.nombre}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (((50, 50, 50))), 2)
                cv2.putText(canvas, f"{CATEGORIAS_DICT.get(letra.categoria, '')}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                if texto_sin_tilde == 'Dificil':
                    cv2.putText(canvas, f"Dificultad: {texto_sin_tilde}", (800, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                elif texto_sin_tilde == 'Media':
                    cv2.putText(canvas, f"Dificultad: {texto_sin_tilde}", (800, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                elif texto_sin_tilde == 'Facil':
                    cv2.putText(canvas, f"Dificultad: {texto_sin_tilde}", (800, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # convertir a JPEG y enviar como respuesta
            ret, jpeg = cv2.imencode('.jpg', canvas)
            if not ret:
                continue

            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

    return StreamingHttpResponse(gen(), content_type='multipart/x-mixed-replace; boundary=frame')





def set_voice_command(text: str | None):
    _cmd_port.set(text)


def clear_canvas(request):
    _cmd_port.set("limpiar pantalla")
    return JsonResponse({"status": "ok"})


@require_POST
def set_color(request):
    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "error": "invalid_payload"}, status=400)
    color = payload.get("color")
    if not color:
        return JsonResponse({"status": "error", "error": "color_required"}, status=400)
    if _loop.set_color(color):
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error", "error": "color_invalid"}, status=400)


@require_POST
def set_grosor(request):
    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "error": "invalid_payload"}, status=400)
    grosor = payload.get("grosor")
    if not grosor:
        return JsonResponse({"status": "error", "error": "grosor_required"}, status=400)

    # Intentar aplicar cambio directamente en _loop si existe una API
    ok = False
    try:
        if hasattr(_loop, "set_thickness"):
            ok = _loop.set_thickness(grosor)
        elif hasattr(_loop, "set_brush_size"):
            ok = _loop.set_brush_size(grosor)
        elif hasattr(_loop, "set_grosor"):
            ok = _loop.set_grosor(grosor)
        else:
            # Fallback: enviar comando de voz al loop (si el loop procesa comandos de texto)
            _cmd_port.set(f"grosor {grosor}")
            ok = True
    except Exception:
        ok = False

    if ok:
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error", "error": "grosor_invalid"}, status=400)