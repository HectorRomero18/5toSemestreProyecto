from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from functools import wraps
from airwrite.infrastructure.models.letra import Letra
from airwrite.infrastructure.models.silabas import Silaba
from airwrite.infrastructure.models.numeros import Numero
from airwrite.domain.services.bloquear import esta_bloqueada


def requiere_desbloqueo(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        perfil = getattr(request.user, 'perfilusuario', None)
        if not perfil:
            return JsonResponse({"error": "Debes tener un perfil para acceder."}, status=403)

        # Detectar qué tipo de objeto se está solicitando
        letra_id = kwargs.get('letra_id')
        silaba_id = kwargs.get('silaba_id')
        numero_id = kwargs.get('numero_id')

        # Caso: Letra
        if letra_id:
            objeto = get_object_or_404(Letra, id=letra_id)
            desbloqueada = not esta_bloqueada(request.user, objeto.nombre)
            tipo = "letra"

        # Caso: Sílaba
        elif silaba_id:
            objeto = get_object_or_404(Silaba, id=silaba_id)
            desbloqueada = (
                objeto.nombre in ["Silaba ba", "Silaba be", "Silaba ca"] or
                objeto in perfil.silabas_desbloqueadas.all()
            )
            tipo = "silaba"

        # Caso: Número (siempre desbloqueado)
        elif numero_id:
            objeto = get_object_or_404(Numero, id=numero_id)
            desbloqueada = True
            tipo = "numero"

        else:
            return JsonResponse({"error": "No se pudo determinar el tipo de objeto."}, status=400)

        # Bloqueo si no está desbloqueado
        if not desbloqueada:
            return JsonResponse({
                "error": f"No tienes esta {tipo} desbloqueada"
            }, status=403)

        return view_func(request, *args, **kwargs)
    return _wrapped_view
