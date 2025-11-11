import json
import cv2
import numpy as np
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from airwrite.interfaces.django_views.trazos import _canvas_port


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

            print("\n=== PETICIÓN A CAPTURAR TRAZO ===")
            print(f"Letra solicitada: {letra}")
            print(f"Usuario: {usuario}")
            print("=================================\n")

            if not letra:
                return JsonResponse({"error": "Debe especificarse la letra."}, status=400)

            canvas_img = _canvas_port.get_canvas()
            if canvas_img is None or canvas_img.size == 0:
                return JsonResponse({"error": "Canvas vacío o no disponible."}, status=400)

            gray = cv2.cvtColor(canvas_img, cv2.COLOR_BGR2GRAY)
            _, binary = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)
            
            if cv2.countNonZero(binary) == 0:
                return JsonResponse({"error": "No hay trazo dibujado en el canvas."}, status=400)

            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            if not contours:
                return JsonResponse({"error": "No se detectaron contornos en el canvas."}, status=400)

            best_contour = max(contours, key=cv2.contourArea)
            points = best_contour.squeeze()
            if len(points.shape) == 1:
                points = np.array([points])

            pts = points.reshape(-1, 2).astype(np.float64)
            
            if len(pts) < 2:
                return JsonResponse({"error": "Trazo demasiado pequeño."}, status=400)

            diffs = np.linalg.norm(pts[1:] - pts[:-1], axis=1)
            dists = np.concatenate(([0.0], diffs))
            cum = np.cumsum(dists)
            total = cum[-1]
            
            if total == 0:
                return JsonResponse({"error": "Trazo sin longitud."}, status=400)

            alphas = np.linspace(0, total, 64, endpoint=False)
            sampled = []
            j = 0
            for a in alphas:
                while j < len(cum) - 1 and cum[j + 1] < a:
                    j += 1
                denom = cum[j + 1] - cum[j] if cum[j + 1] != cum[j] else 1e-6
                t = (a - cum[j]) / denom
                p = (1 - t) * pts[j] + t * pts[j + 1]
                sampled.append(p)

            sampled = np.array(sampled)
            pts_min = sampled.min(axis=0)
            pts_max = sampled.max(axis=0)
            scale = 240 / max(pts_max - pts_min)
            pts_scaled = (sampled - pts_min) * scale + 8
            coordenadas = [(int(x), int(y)) for x, y in pts_scaled]

            return JsonResponse({
                "mensaje": f"Trazo capturado exitosamente para la letra '{letra}'.",
                "letra": letra,
                "usuario": usuario,
                "trazo": [{"x": x, "y": y} for x, y in coordenadas]
            }, status=200)

        except Exception as e:
            print("\n❌ ERROR EN CAPTURAR_TRAZO:", str(e))
            return JsonResponse({"error": str(e)}, status=500)
