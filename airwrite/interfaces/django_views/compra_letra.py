from django.views.decorators.http import require_POST
from django.http import JsonResponse
from airwrite.application.use_cases.compra_letra import CompraLetraUseCase, ComprarLetraCommand
from airwrite.infrastructure.repositories.compra_letra import DjangoPerfilRepository, DjangoLetraCompraRepository

@require_POST
def comprar_letra(request):
    try:
        # Obtener datos del POST
        letra = request.POST.get('letra')
        precio = int(request.POST.get('precio', 0))
        user_id = request.user.id  # id del usuario actual

        # Repositorios
        perfil_repo = DjangoPerfilRepository()
        compra_repo = DjangoLetraCompraRepository()

        # Use case
        use_case = CompraLetraUseCase(perfil_repo=perfil_repo, compra_repo=compra_repo)

        # Crear comando
        command = ComprarLetraCommand(
            user_id=user_id,  # Use case usará este ID para obtener la entidad Usuario
            letra=letra,
            precio=precio
        )

        # Ejecutar compra
        result = use_case.execute(command)

        # Obtener el XP actualizado
        perfil_actualizado = perfil_repo.get_perfil(request.user.id)
        nuevo_xp = perfil_actualizado.xp

        return JsonResponse({
            "success": True,
            "message": result["msg"],
            "user_xp": nuevo_xp 
        })

    except Exception as e:
        # Devolver JSON con error
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
