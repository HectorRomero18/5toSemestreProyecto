from django.views.generic import TemplateView

from airwrite.application.use_cases.list_letras import (
   ListLetrasQuery,
   ListLetrasUseCase, 
)
from airwrite.infrastructure.repositories.django_letra_repository import (
    DjangoLetraRepository
)
from django.contrib.auth.mixins import LoginRequiredMixin
from airwrite.domain.constants.xp_reward import DIFICULTADES, CATEGORIAS_LETRAS
from airwrite.infrastructure.models.letra_compra import LetraCompra

DIFICULTADES_DICT = dict(DIFICULTADES)
CATEGORIAS_LETRAS_DICT = dict(CATEGORIAS_LETRAS)

class TiendaXpListView( LoginRequiredMixin, TemplateView):
    template_name = 'airwrite/tiendaXp/tiendaXp.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q')

        repo = DjangoLetraRepository()
        use_case = ListLetrasUseCase(repo)
        user = self.request.user
        compradas = LetraCompra.objects.filter(usuario=user).values_list('letra__nombre', flat=True)
        compradas = [c.lower() for c in compradas]
        print("Letras compradas:", compradas)

        modules = use_case.execute(ListLetrasQuery(q=q))
        perfil = getattr(user, 'perfilusuario', None)
        # Convertir cada LetraEntity a dict
        modules_serializable = [
            {

                'id':  m.id,
                'letter': m.caracter.lower(),
                'categoria': CATEGORIAS_LETRAS_DICT.get(m.categoria, ''),
                'dificultad': DIFICULTADES_DICT.get(m.dificultad, ''),
                'price': m.precio_xp,
                'letra_obj': m.caracter[-1],
                'simbolo': m.caracter

            }
            for m in modules
        ]
        print(type(modules_serializable[0]['letter'])) 


        user_xp = perfil.xp if perfil else 0
        context.update({'modules': modules_serializable, 'title': 'Module List', 'user': user, 'user_xp': user_xp, 'compradas': list(compradas)})
        return context