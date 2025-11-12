from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from airwrite.application.use_cases.compra_letra import CompraLetraUseCase, ComprarLetraCommand
from airwrite.infrastructure.repositories.compra_letra import DjangoPerfilRepository, DjangoLetraCompraRepository
from airwrite.infrastructure.models.letra_compra import LetraCompra
# Añadir import del modelo Letra
from airwrite.infrastructure.models.letra import Letra
 
@require_POST
@login_required
def comprar_letra(request):
    try:
        letra = (request.POST.get('letra') or '').strip()
        precio = int(request.POST.get('precio', 0))
        user_id = request.user.id

        # Resolver la instancia Letra antes de ejecutar el use case
        letra_obj = None
        if not letra:
            return JsonResponse({'success': False, 'message': 'Parámetro letra requerido'}, status=400)

        # Intentar por PK si es dígito, si no por campos comunes (nombre, caracter, simbolo)
        try:
            if letra.isdigit():
                letra_obj = Letra.objects.exclude(nombre__in=["Letra A", "Letra B", "Letra C"]).filter(pk=int(letra)).first()
            if letra_obj is None:
                letra_obj = Letra.objects.exclude(nombre__in=["Letra A", "Letra B", "Letra C"]).filter(nombre__iexact=letra).first()
            if letra_obj is None:
                letra_obj = Letra.objects.exclude(nombre__in=["Letra A", "Letra B", "Letra C"]).filter(caracter__iexact=letra).first()
            if letra_obj is None:
                letra_obj = Letra.objects.exclude(nombre__in=["Letra A", "Letra B", "Letra C"]).filter(simbolo__iexact=letra).first()

        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error al buscar letra: {e}'}, status=500)

        if letra_obj is None:
            return JsonResponse({'success': False, 'message': 'Letra no encontrada'}, status=404)
        

        perfil_repo = DjangoPerfilRepository()
        compra_repo = DjangoLetraCompraRepository()
        use_case = CompraLetraUseCase(perfil_repo=perfil_repo, compra_repo=compra_repo)

        # Pasar la instancia de Letra al comando (así no se asigna una cadena al FK)
        command = ComprarLetraCommand(user_id=user_id, letra=letra_obj, precio=precio)
        result = use_case.execute(command)

        # obtener lista actualizada de compradas desde el modelo
        compradas_qs = LetraCompra.objects.filter(usuario=request.user).values_list('letra__nombre', flat=True)
        compradas = [c.lower() for c in compradas_qs]

        perfil_actualizado = perfil_repo.get_perfil(request.user.id)
        nuevo_xp = perfil_actualizado.xp

        return JsonResponse({
            "success": True,
            "message": result.get("msg", ""),
            "user_xp": nuevo_xp,
            "compradas": compradas
        })

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
