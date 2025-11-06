from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from airwrite.application.use_cases.list_silabas import (
    ListSilabasUseCase,
    ListSilabasQuery,
)
from airwrite.infrastructure.repositories.django_silaba_repository import (
    DjangoSilabaRepository,
)
from airwrite.domain.constants.xp_reward import DIFICULTADES
from airwrite.domain.services.bloquear_silaba import esta_bloqueada_silaba


# Convertimos la tupla DIFICULTADES en un diccionario para fácil acceso
DIFICULTADES_DICT = dict(DIFICULTADES)


class SilabaListView(LoginRequiredMixin, TemplateView):
    template_name = 'airwrite/modules/silaba.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Parámetro de búsqueda opcional (GET)
        q = self.request.GET.get('q')

        # Inicializamos el repositorio y caso de uso
        repo = DjangoSilabaRepository()
        use_case = ListSilabasUseCase(repo=repo)

        # Obtenemos el usuario actual
        user = self.request.user

        # Ejecutamos el caso de uso con la consulta
        modules = use_case.execute(ListSilabasQuery(q=q))

        # Convertimos cada SilabaEntity a un diccionario serializable
        modules_serializable = []
        for m in modules:
            modules_serializable.append({
                'id': m.id,
                'silaba': m.nombre[-2:],
                'bloqueada': esta_bloqueada_silaba(user, m.nombre),
                'dificultad': DIFICULTADES_DICT.get(m.dificultad, ''),
                'price': getattr(m, 'price', 100),
                'simbolo': m.nombre,
            })
            

        # Obtenemos la experiencia del usuario (xp)
        perfil = getattr(user, 'perfilusuario', None)
        user_xp = perfil.xp if perfil else 0

        # Actualizamos el contexto para la plantilla
        context.update({
            'modules': modules_serializable,
            'title': 'Module List',
            'user': user,
            'user_xp': user_xp,
        })

        return context
