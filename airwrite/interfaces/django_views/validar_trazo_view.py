import json
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from airwrite.domain.entities.trazo import Trazo
from airwrite.domain.entities.usuario import Usuario
from airwrite.application.use_cases.validar_escritura import ValidadorEscrituraUseCase
from airwrite.infrastructure.storage.letra_storage import LetraStorage
from airwrite.infrastructure.repositories.canvas_with_trace import CanvasAdapterWithTrace

@method_decorator(csrf_exempt, name='dispatch')
class ValidarTrazoView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Instancia de LetraStorage (carga letras desde 'media/')
        self.storage = LetraStorage(carpeta_media="media")
        self.storage.cargar_letras()
    def post(self, request, *args, **kwargs):
        try:
            # --- 1️ Parsear el JSON recibido ---
            data = json.loads(request.body.decode("utf-8"))
            caracter = data.get("caracter", "").upper()
            coords_usuario = data.get("coordenadas", [])
            nombre_usuario = data.get("usuario", "Anonimo")

            # 🧭 Depuración temporal
            print("\n--- PETICIÓN RECIBIDA EN VALIDAR_TRAZO ---")
            print("Letra recibida:", caracter)
            print("Primeras coordenadas:", coords_usuario[:5])
            print("Total de puntos:", len(coords_usuario))
            print("------------------------------------------\n")

            if not caracter or not coords_usuario:
                return JsonResponse(
                    {"error": "Faltan datos: caracter o coordenadas."}, status=400
                )

            # --- 2️ Obtener trazo de referencia ---
            letra_ref = self.storage.obtener_letra(caracter)
            if not letra_ref or not letra_ref.trazos:
                return JsonResponse(
                    {"error": f"No se encontró la letra '{caracter}' o no tiene trazos."},
                    status=404,
                )

            # Si el front envía [{x:…, y:…}], convertir a [(x,y)]
            if isinstance(coords_usuario[0], dict):
                coords_usuario = [(pt["x"], pt["y"]) for pt in coords_usuario]

            # --- 3️ Crear trazo del usuario ---
            adapter = CanvasAdapterWithTrace()
            coords_normalizadas = adapter._normalize_points(coords_usuario, target_size=256, pad=8)
            trazo_usuario = Trazo(coordenadas=coords_normalizadas)

            # --- 4️ Ejecutar el caso de uso de validación ---
            usuario = Usuario(nombre=nombre_usuario)
            validador = ValidadorEscrituraUseCase(usuario=usuario, umbral_similitud=0.85)
            resultado = validador.ejecutar_validacion(letra_ref, trazo_usuario)

            # --- 5️ Devolver respuesta JSON ---
            return JsonResponse({
                "caracter": caracter,
                "usuario": nombre_usuario,
                "resultado": resultado,
                "coordenadas_usuario": coords_normalizadas,
                "coordenadas_referencia": letra_ref.trazos[0].coordenadas if letra_ref.trazos else [],
                "mensaje": f"Validación completada para la letra '{caracter}'."
            }, status=200)

        except Exception as e:
            print("\n❌ ERROR EN VALIDAR_TRAZO:", str(e))
            return JsonResponse({"error": str(e)}, status=500)


# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json

# from airwrite.infrastructure.repositories.canvas_with_trace import CanvasAdapterWithTrace
# from airwrite.domain.entities.usuario import Usuario
# from airwrite.domain.entities.letra import LetraEntity
# from airwrite.application.use_cases.validar_escritura import ValidadorEscrituraUseCase

# # Mantener CSRF protegido si se llama desde JS con token
# @csrf_exempt
# def validar_trazo(request):
#     if request.method != "POST":
#         return JsonResponse({"error": "Método no permitido"}, status=405)

#     try:
#         data = json.loads(request.body)
#         caracter = data.get("caracter")
#         coordenadas = data.get("coordenadas", [])

#         if not caracter or not coordenadas:
#             return JsonResponse({"error": "Faltan datos de trazo"}, status=400)

#         # Inicializar CanvasAdapter con estado vacío (o imagen de fondo si se usa)
#         canvas = CanvasAdapterWithTrace(state=None, N_points=64)
#         # Agregar los puntos recibidos desde JS
#         for x, y in coordenadas:
#             canvas._maybe_append_point((x, y))

#         # Generar payload con letra seleccionada y usuario simulado
#         payload = canvas.trace_to_payload(usuario="UsuarioPrueba", letra=caracter)

#         # Validar trazo usando el use_case
#         validador = ValidadorEscrituraUseCase()
#         resultado = validador.validar_trazo(payload)  # Devuelve dict con similitud, correcto, etc.

#         return JsonResponse({"resultado": resultado, "caracter": caracter})

#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)
