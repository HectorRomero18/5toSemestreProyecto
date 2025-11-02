from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from airwrite.application.use_cases.compra_letra import CompraLetraUseCase, ComprarLetraCommand
from airwrite.infrastructure.repositories.compra_letra import DjangoPerfilRepository, DjangoLetraCompraRepository
from airwrite.infrastructure.models.letra_compra import LetraCompra

@require_POST
@login_required
def comprar_letra(request):
    try:
        letra = (request.POST.get('letra') or '').strip()
        precio = int(request.POST.get('precio', 0))
        user_id = request.user.id

        perfil_repo = DjangoPerfilRepository()
        compra_repo = DjangoLetraCompraRepository()
        use_case = CompraLetraUseCase(perfil_repo=perfil_repo, compra_repo=compra_repo)

        command = ComprarLetraCommand(user_id=user_id, letra=letra, precio=precio)
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
