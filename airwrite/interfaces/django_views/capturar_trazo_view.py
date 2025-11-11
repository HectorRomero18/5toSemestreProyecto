import json
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from airwrite.infrastructure.repositories.canvas_with_trace import CanvasAdapterWithTrace


@method_decorator(csrf_exempt, name="dispatch")
class CapturarTrazoView(View):
    """
    Vista que activa la cámara, captura el trazo con marcador azul y
    devuelve las coordenadas normalizadas como JSON.
    """

    def post(self, request, *args, **kwargs):
        try:
            # 1️⃣ Parsear datos del body
            data = json.loads(request.body.decode("utf-8"))
            letra = data.get("letra", "").strip().upper()
            usuario = data.get("usuario", "Anonimo")

            print("\n=== PETICIÓN A CAPTURAR TRAZaO ===")
            print(f"Letra solicitada: {letra}")
            print(f"Usuario: {usuario}")
            print("=================================\n")

            if not letra:
                return JsonResponse({"error": "Debe especificarse la letra."}, status=400)

            # 2️⃣ Instanciar el adaptador y capturar trazo con cámara
            adapter = CanvasAdapterWithTrace()
            payload = adapter.capture_trazo_camera(letra=letra, usuario=usuario)

            # 3️⃣ Devolver los puntos capturados
            return JsonResponse({
                "mensaje": f"Trazo capturado exitosamente para la letra '{letra}'.",
                "letra": payload["letra"],
                "usuario": payload["usuario"],
                "trazo": payload["trazo"]
            }, status=200)

        except Exception as e:
            print("\n❌ ERROR EN CAPTURAR_TRAZO:", str(e))
            return JsonResponse({"error": str(e)}, status=500)
