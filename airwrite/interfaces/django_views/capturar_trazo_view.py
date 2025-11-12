import json
import cv2
import numpy as np
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from airwrite.interfaces.django_views.trazos import _canvas_port, _loop


@method_decorator(csrf_exempt, name="dispatch")
class CapturarTrazoView(View):
    """
    Vista que extrae el trazo del canvas actual sin abrir una nueva cámara.
    """

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode("utf-8"))
            letra = data.get("letra", "").strip().upper()
            usuario = data.get("usuario", "Anonimo")

            import logging
            logger = logging.getLogger(__name__)
            logger.info(f"Capturando trazo para letra: {letra}, usuario: {usuario}")

            if not letra:
                return JsonResponse({"error": "Debe especificarse la letra."}, status=400)

            # Obtener las coordenadas del trazo del usuario desde el loop
            coordenadas = _loop.get_user_trace()
            if not coordenadas:
                return JsonResponse({"error": "No hay trazo capturado."}, status=400)

            logger.info(f"Trazo capturado: {len(coordenadas)} puntos")

            # Limpiar el trazo después de capturarlo
            _loop.state.user_trace = []

            return JsonResponse({
                "mensaje": f"Trazo capturado exitosamente para la letra '{letra}'.",
                "letra": letra,
                "usuario": usuario,
                "trazo": [{"x": x, "y": y} for x, y in coordenadas]
            }, status=200)

        except Exception as e:
            print("\n❌ ERROR EN CAPTURAR_TRAZO:", str(e))
            return JsonResponse({"error": str(e)}, status=500)
