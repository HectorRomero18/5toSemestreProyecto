from django.views.generic import TemplateView

from airwrite.application.use_cases.list_letras import (
    ListLetrasQuery,
    ListLetrasUseCase,
)
from airwrite.infrastructure.repositories.django_letra_repository import (
    DjangoLetraRepository,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from airwrite.domain.constants.xp_reward import DIFICULTADES



# views.py

DIFICULTADES_DICT = dict(DIFICULTADES)
class AbecedarioListView(LoginRequiredMixin, TemplateView):
    template_name = 'airwrite/modules/abecedario.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q')

        repo = DjangoLetraRepository()
        use_case = ListLetrasUseCase(repo=repo)
        user = self.request.user

        modules = use_case.execute(ListLetrasQuery(q=q))
        
        # Convertir cada LetraEntity a dict
        modules_serializable = [
            {
                'letter': m.caracter,
                'categoria': getattr(m, 'categoria', ''),
                'dificultad': DIFICULTADES_DICT.get(m.dificultad, ''),
                'price': getattr(m, 'price', 100),  # si tienes un precio
                'simbolo': m.caracter[-1]

            }
            for m in modules
        ]

        perfil = getattr(user, 'perfilusuario', None)
        user_xp = perfil.xp if perfil else 0

        context.update({
            'modules': modules_serializable,
            'title': 'Module List',
            'user': user,
            'user_xp': user_xp
        })
        return context
