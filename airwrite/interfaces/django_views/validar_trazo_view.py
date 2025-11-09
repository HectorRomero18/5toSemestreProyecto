import json
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from airwrite.domain.entities.trazo import Trazo
from airwrite.application.use_cases.validar_escritura import ValidadorEscrituraUseCase
from airwrite.infrastructure.storage.letra_storage import LetraStorage


@method_decorator(csrf_exempt, name='dispatch')
class ValidarTrazoView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Instancia de LetraStorage (carga letras desde 'media/')
        self.storage = LetraStorage(carpeta_media="media")

    def post(self, request, *args, **kwargs):
        try:
            # --- 1️ Parsear el JSON recibido ---
            data = json.loads(request.body.decode("utf-8"))
            caracter = data.get("caracter", "").upper()
            coords_usuario = data.get("coordenadas", [])

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
                    {"error": f"No se encontró trazo de referencia para '{caracter}'."},
                    status=404,
                )

            trazo_referencia = letra_ref.trazos[0]

            # --- 3️ Crear trazo del usuario ---
            trazo_usuario = Trazo(coordenadas=coords_usuario)

            # --- 4️ Ejecutar el caso de uso de validación ---
            validador = ValidadorEscrituraUseCase()
            resultado = validador.ejecutar(trazo_usuario, trazo_referencia)

            # --- 5️ Devolver respuesta JSON ---
            return JsonResponse({
                "caracter": caracter,
                "resultado": resultado,
                "mensaje": f"Validación completada para la letra '{caracter}'."
            })

        except Exception as e:
            print("\n❌ ERROR EN VALIDAR_TRAZO:", str(e))
            return JsonResponse({"error": str(e)}, status=500)
