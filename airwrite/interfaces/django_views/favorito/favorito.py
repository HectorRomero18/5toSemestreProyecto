# Vistas de favoritos
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from airwrite.application.use_cases.favorito.favorito_use_case import (
     ListFavoritosQuery,
     ListFavoritosUseCase,
     AddFavoritoUseCase,
     AddFavoritoCommand,
     DeleteFavoritoUseCase,
     DeleteFavoritoCommand,
     ExistsFavoritoUseCase,
     ExistsFavoritoQuery
    
)
from airwrite.infrastructure.repositories.favorito.favorito_repository import (
    DjangoFavoritoRepository
)

from django.contrib.auth.mixins import LoginRequiredMixin
import json

from airwrite.infrastructure.models import Letra

@login_required
class FavoritoListView( LoginRequiredMixin, TemplateView):
    template_name = 'airwrite/modules/favorito.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q')

        repo = DjangoFavoritoRepository()
        use_case = ListFavoritosUseCase(repo)
        user = self.request.user

        user_perfil_id = getattr(self.request.user, 'perfilusuario', None).id
        modules = use_case.execute(ListFavoritosQuery(q=q, user_id=user_perfil_id))

        modules_list = []
        for f in modules:
            letra_nombre = f.letra_nombre

            tipo = 'V' if letra_nombre[-1].upper() in 'AEIOU' else 'C'
            bg = 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-1.png' if tipo == 'V' else 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png'
            modules_list.append({
                'id': f.id,
                'letra_id': f.letra_id,
                'user_id': f.user_id,
                'letter': f.letra_nombre,
                'dificultad': f.letra_dificultad,
                'simbolo': f.letra_nombre[-1],
                'tipo': tipo,
                'bg': bg
            })
        # print(modules_list)

        context['modules'] = modules_list
        return context
    
    

@method_decorator(csrf_exempt, name='dispatch')
class FavoritoAddView(LoginRequiredMixin, View):
    """ Agregar una letra a favoritos """
    
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            print("Data recibida:", data)
            
            letra_id = data.get('letra_id')
            nombre = data.get('nombre')
            
            print(f"letra_id: {letra_id}, nombre: {nombre}")
            
            # Si no hay letra_id, buscar por nombre
            if not letra_id and nombre:
                try:
                    letra = Letra.objects.get(nombre__iexact=nombre)
                    letra_id = letra.id
                    print(f"Letra encontrada por nombre: {letra_id}")
                except Letra.DoesNotExist:
                    return JsonResponse({
                        'status': False,
                        'error': f'Letra con nombre "{nombre}" no encontrada'
                    }, status=404)
                except Exception as e:
                    return JsonResponse({
                        'status': False,
                        'error': f'Error al buscar letra: {str(e)}'
                    }, status=500)
            
            if not letra_id:
                return JsonResponse({
                    'status': False,
                    'error': 'letra_id o nombre es requerido'
                }, status=400)
            
            if not hasattr(request.user, 'perfilusuario'):
                return JsonResponse({
                    'status': False,
                    'error': 'El usuario no tiene un perfil asociado'
                }, status=400)
            
            user_id = request.user.perfilusuario.id

            repo = DjangoFavoritoRepository()
            use_case = AddFavoritoUseCase(repo)
            comando = AddFavoritoCommand(letra_id=letra_id, user_id=user_id)
            favorito = use_case.execute(comando)

            return JsonResponse({
                'status': True,
                'favorito': {
                    'id': favorito.id,
                    'user_id': user_id,
                    'letra_id': favorito.letra_id
                }
            })
            
        except json.JSONDecodeError as e:
            return JsonResponse({
                'status': False,
                'error': f'JSON inválido: {str(e)}'
            }, status=400)
            
        except Exception as e:
            import traceback
            print("Error completo:", traceback.format_exc())
            return JsonResponse({
                'status': False,
                'error': f'Error: {str(e)}'
            }, status=500)

class FavoritoDeleteView(LoginRequiredMixin, View):
    """ Eliminar una letra de favoritos """
    def post(self, request, *args, **kwargs):
        #  Parsear el cuerpo del request como JSON
        data = json.loads(request.body)
        letra_id = int(data.get('letra_id'))
        user_id = request.user.perfilusuario.id

        #  Ejecutar el caso de uso
        repo = DjangoFavoritoRepository()
        use_case = DeleteFavoritoUseCase(repo)
        comando = DeleteFavoritoCommand(letra_id=letra_id, user_id=user_id)
        use_case.execute(comando)

        # Devolver respuesta JSON
        return JsonResponse({'status': True})
    
class FavoritoExistsView(LoginRequiredMixin, View):
    """ Verificar si existe un favorito """
    def get(self, request, *args, **kwargs):
        letra_id = self.request.GET.get('letra_id')
        user_id = self.request.user.perfilusuario.id

        repo = DjangoFavoritoRepository()
        use_case = ExistsFavoritoUseCase(repo)
        query = ExistsFavoritoQuery(letra_id=letra_id, user_id=user_id)
        exists = use_case.execute(query)

        return JsonResponse({'exists': exists})