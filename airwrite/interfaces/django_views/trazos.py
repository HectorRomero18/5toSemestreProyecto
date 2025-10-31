from django.http import StreamingHttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import cv2
import time
import json

from django.views.decorators.http import require_POST

from airwrite.application.use_cases.drawing_loop import DrawingLoop, DrawingConfig, DrawingState
from airwrite.infrastructure.repositories.state import OpenCVCamera, CanvasState, CommandState
from airwrite.infrastructure.repositories.adapters import CameraAdapter, CanvasAdapter, CommandAdapter


_camera = OpenCVCamera(index=1)
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
)
_state = DrawingState()
_loop = DrawingLoop(_cam_port, _canvas_port, _cmd_port, _cfg, _state)


@login_required
def index(request):
    # Usar plantilla en airwrite/templates/airwrite/index.html
    return render(request, 'airwrite/index.html')


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


def video_feed_canvas(request):
    def gen():
        while True:
            _lazy_start()
            
            _loop.step()
            canvas = _canvas_port.get()
            if canvas is None:
                time.sleep(0.01)
                continue
            cv2.putText(canvas, "A", (100, 300),cv2.FONT_HERSHEY_SIMPLEX, 10, (255,255,255), 10, cv2.LINE_AA)
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