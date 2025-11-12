# airwrite/interface/django_views/validador_trazo_view.py
import base64
import cv2
import numpy as np
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View

# IMPORTS — ajusta rutas si tus módulos quedaron en otro sitio
# reiniciar_lienzo: crea base_canvas y modelo_gray (usa generar_modelo_texto internamente)
# evaluar_trazo_por_contorno: devuelve (score, overlay_bgr)
from airwrite.infrastructure.opencv.trazo_extractor import reiniciar_lienzo
from airwrite.domain.services.evaluar_trazo import evaluar_trazo_por_contorno


def _b64_to_cv2_img(b64string):
    # acepta "data:image/png;base64,..." o solo el base64
    if b64string.startswith("data:"):
        b64string = b64string.split(",", 1)[1]
    img_data = base64.b64decode(b64string)
    nparr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


def _cv2_img_to_datauri_png(img):
    _, buff = cv2.imencode(".png", img)
    b64 = base64.b64encode(buff).decode("utf-8")
    return f"data:image/png;base64,{b64}"


@method_decorator(csrf_exempt, name="dispatch")
class ValidarTrazoApiView(View):
    """
    POST expected JSON:
      { "image_base64": "data:image/png;base64,...", "texto": "A" }
    or multipart/form-data with file field 'image' and optional 'texto'.
    Response:
      { "score": 92.5, "overlay": "data:image/png;base64,..." }
    """
    def post(self, request, *args, **kwargs):
        # 1) obtener texto objetivo
        texto = request.POST.get("texto") or (request.GET.get("texto") or "A")

        # 2) obtener imagen (file o base64)
        img_file = request.FILES.get("image")
        img_b64 = request.POST.get("image_base64") or (request.body and None)

        frame = None
        if img_file:
            data = img_file.read()
            nparr = np.frombuffer(data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        else:
            # intenta leer JSON body si es JSON
            # si te mandan JSON con image_base64, Django no lo pone en POST; tenemos que parsearlo.
            try:
                import json
                payload = json.loads(request.body.decode("utf-8"))
                img_b64 = payload.get("image_base64") or img_b64
                texto = payload.get("texto") or texto
            except Exception:
                pass
            if img_b64:
                frame = _b64_to_cv2_img(img_b64)

        if frame is None:
            return JsonResponse({"error": "No se recibió imagen. Enviar 'image' (file) o 'image_base64' (string)."}, status=400)

        # 3) preparar base/modelo y evaluar
        base_canvas, modelo_gray = reiniciar_lienzo(frame.shape, texto)
        score, overlay = evaluar_trazo_por_contorno(frame, base_canvas, modelo_gray)

        overlay_datauri = _cv2_img_to_datauri_png(overlay)

        return JsonResponse({"score": float(score), "overlay": overlay_datauri})
