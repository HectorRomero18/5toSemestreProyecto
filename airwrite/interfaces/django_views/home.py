from django.views.generic import TemplateView

from airwrite.application.use_cases.list_modules import (
    ListModulesUseCase,
    ListModulesQuery,
)
from airwrite.infrastructure.repositories.django_module_repository import (
    DjangoModuleRepository,
)
from django.contrib.auth.mixins import LoginRequiredMixin



class ModuleListView( LoginRequiredMixin, TemplateView):
    template_name = 'airwrite/home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q')

        repo = DjangoModuleRepository()
        use_case = ListModulesUseCase(repo)
        user = self.request.user
        perfil = getattr(user, 'perfilusuario', None)
        # user_favoritos = [f.letra for f in perfil.favoritos.all()] if perfil else []


        modules = use_case.execute(ListModulesQuery(q=q))
        for m in modules:
            if m.imagen_url:  # verifica que exista imagen
                print(m.imagen_url)
            else:
                print(f"{m.name} no tiene imagen.")


        user_xp = perfil.xp if perfil else 0
        context.update({'modules': modules, 
                        'title': 'Module List', 
                        'user': user, 'user_xp': user_xp, 
                        'practicadas': perfil.letras_practicadas.all() if perfil else [],
                        'compradas': perfil.user_id.letracompra_set.all()
                                                            if perfil else []
                        })
        return context