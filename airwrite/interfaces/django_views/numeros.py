from django.views.generic import TemplateView

from airwrite.application.use_cases.list_numeros import (
    ListNumerosQuery,
    ListNumerosUseCase
)
from airwrite.infrastructure.repositories.numeros.django_numero_repository import (
    DjangoNumeroRepository,
)
from django.contrib.auth.mixins import LoginRequiredMixin

from airwrite.domain.constants.xp_reward import DIFICULTADES

DIFICULTADES_DICT = dict(DIFICULTADES)

class NumeroListView(LoginRequiredMixin, TemplateView):
    template_name = 'airwrite/modules/numeros.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q')

        repo = DjangoNumeroRepository()
        use_case = ListNumerosUseCase(repo)
        user = self.request.user
        
        numeros = use_case.execute(ListNumerosQuery(q=q))  # esto devuelve objetos NumeroEntity

        modules_list = []
        for n in numeros:
            modules_list.append({
                'id': n.id,
                'numero': n.caracter,       
                'dificultad': DIFICULTADES_DICT.get(n.dificultad, ''),
                'simbolo': n.caracter[-1]   
            })

        perfil = getattr(user, 'perfilusuario', None)
        user_xp = perfil.xp if perfil else 0

        context.update({
            'modules': modules_list,
            'title': 'Module List',
            'user': user,
            'user_xp': user_xp
        })
        return context
