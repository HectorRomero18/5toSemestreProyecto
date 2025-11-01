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
    template_name = 'airwrite/modules/silaba.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q')

        repo = DjangoModuleRepository()
        use_case = ListModulesUseCase(repo)
        user = self.request.user
        
        modules = use_case.execute(ListModulesQuery(q=q))
        perfil = getattr(user, 'perfilusuario', None)

        user_xp = perfil.xp if perfil else 0
        context.update({'modules': modules, 'title': 'Module List', 'user': user, 'user_xp': user_xp})
        return context