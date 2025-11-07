from django.views.generic import TemplateView

from airwrite.application.use_cases.list_letras_compradas import (
    ListLetrasQuery,
    ListLetrasUseCase
)
from airwrite.infrastructure.repositories.django_letras_compradas_repository import (
    DjangoLetrasCompradasList,
)
from django.contrib.auth.mixins import LoginRequiredMixin



class CompradaListView(LoginRequiredMixin, TemplateView):
    template_name = 'airwrite/modules/comprada.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q')

        repo = DjangoLetrasCompradasList()
        use_case = ListLetrasUseCase(repo)
        user = self.request.user
        
        modules = use_case.execute(ListLetrasQuery(q=q))

        modules_list = []

        for m in modules:
            
            if m.usuario != user:
                continue  # saltar letras de otros usuarios
            
            letra_nombre = m.letra.nombre
            
            # Determinar tipo según si es vocal o consonante
            tipo = 'V' if letra_nombre[-1].upper() in 'AEIOU' else 'C'

            # URL de imagen de fondo según tipo
            bg = 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-1.png' if tipo == 'V' else 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png'

            modules_list.append({
                'usuario': user.username,
                'letra': letra_nombre,
                'precio': m.precio,
                'fecha': m.fecha.isoformat(),
                'tipo': tipo,
                'bg': bg,
                'simbolo': letra_nombre[-1]
            })

        perfil = getattr(user, 'perfilusuario', None)
        context.update({'modules': modules_list, 'title': 'Module List', 'user': user, 'perfil': perfil})
        return context
