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
from airwrite.domain.services.bloquear import esta_bloqueada




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

        perfil = getattr(user, 'perfilusuario', None)

        # Convertir cada LetraEntity a dict
        modules_serializable = []

        for m in modules:

            modules_serializable.append({
                'id': m.id,
                'letter': m.caracter,
                'bloqueada': esta_bloqueada(user, m.caracter),
                'categoria': getattr(m, 'categoria', ''),
                'dificultad': DIFICULTADES_DICT.get(m.dificultad, ''),
                'price': getattr(m, 'price', 100),
                'simbolo': m.caracter[-1],  # para mostrar solo la letra
                'practicada': perfil.letras_practicadas.filter(id=m.id).exists() if perfil else False
            })


        user_xp = perfil.xp if perfil else 0

        context.update({
            'modules': modules_serializable,
            'title': 'Module List',
            'user': user,
            'user_xp': user_xp
        })
        return context
