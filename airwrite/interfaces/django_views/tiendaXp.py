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
        
        modules = use_case.execute(ListLetrasQuery(q=q))
        perfil = getattr(user, 'perfilusuario', None)

        # Convertir cada LetraEntity a dict
        modules_serializable = [
            {
                'letter': m.caracter,
                'categoria': CATEGORIAS_LETRAS_DICT.get(m.categoria, ''),
                'dificultad': DIFICULTADES_DICT.get(m.dificultad, ''),
                'price': m.precio_xp,
                'simbolo': m.caracter[-1]

            }
            for m in modules
        ]


        user_xp = perfil.xp if perfil else 0
        context.update({'modules': modules_serializable, 'title': 'Module List', 'user': user, 'user_xp': user_xp})
        return context