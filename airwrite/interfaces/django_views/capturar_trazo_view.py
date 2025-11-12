from django.http import JsonResponse
import json

def capturar_trazo(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        puntos = data.get('puntos', [])
        print("Trazo recibido:", puntos)
        return JsonResponse({'status': 'ok', 'mensaje': 'Trazo capturado'})
    return JsonResponse({'status': 'error', 'mensaje': 'Método no permitido'})
