from django.http import StreamingHttpResponse, JsonResponse
from django.shortcuts import render
import cv2
import time
import threading

from airwrite.domain.use_cases.drawing_loop import DrawingLoop, DrawingConfig, DrawingState
from airwrite.domain.use_cases.ocr_canvas import recognize_text_from_canvas
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

# Bucle de procesamiento en un hilo de fondo para no recalcular por endpoint
_bg_started = False
_bg_lock = threading.Lock()

def _ensure_background_loop():
    global _bg_started
    with _bg_lock:
        if _bg_started:
            return
        _cam_port.start()
        def run():
            # loop a ~30fps con pequeño sleep para no saturar CPU
            while True:
                try:
                    t0 = time.time()
                    _loop.step()
                    # objetivo 30 fps (~33ms)
                    elapsed = time.time() - t0
                    if elapsed < 0.045:  # ~22 FPS objetivo
                        time.sleep(0.045 - elapsed)
                except Exception:
                    # Evita que el hilo muera por error transitorio
                    time.sleep(0.05)
        th = threading.Thread(target=run, daemon=True)
        th.start()
        _bg_started = True


def index(request):
    _ensure_background_loop()
    return render(request, 'index.html')


def video_feed_cam(request):
    _ensure_background_loop()
    def gen():
        while True:
            frame = _loop.get_last_camera()
            if frame is None:
                time.sleep(0.01)
                continue
            ret, jpeg = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
            if not ret:
                time.sleep(0.01)
                continue
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
            time.sleep(0.01)
    return StreamingHttpResponse(gen(), content_type='multipart/x-mixed-replace; boundary=frame')


def video_feed_canvas(request):
    _ensure_background_loop()
    def gen():
        while True:
            canvas = _canvas_port.get()
            if canvas is None:
                time.sleep(0.01)
                continue
            ret, jpeg = cv2.imencode('.jpg', canvas, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
            if not ret:
                time.sleep(0.01)
                continue
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
            time.sleep(0.01)
    return StreamingHttpResponse(gen(), content_type='multipart/x-mixed-replace; boundary=frame')


def recognize_canvas_text(request):
    """Endpoint: reconoce el texto del canvas actual y lo devuelve como JSON."""
    try:
        text, empty = recognize_text_from_canvas(_canvas_port, languages=['es', 'en'])
        return JsonResponse({
            'ok': True,
            'empty': empty,
            'text': text,
        })
    except Exception as e:  # p. ej. si easyocr no está instalado
        return JsonResponse({'ok': False, 'error': str(e)}, status=500)


# API para voz (integración actual):
# desde voice_assistant, haz: from airwrite.interfaces.django_views.trazos import set_voice_command

def set_voice_command(text: str | None):
    _cmd_port.set(text)