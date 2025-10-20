from django.views.generic import TemplateView

from airwrite.domain.use_cases.list_modules import (
    ListModulesUseCase,
    ListModulesQuery,
)
from airwrite.infrastructure.repositories.django_module_repository import (
    DjangoModuleRepository,
)
from django.contrib.auth.mixins import LoginRequiredMixin



class ModuleListView( LoginRequiredMixin, TemplateView):
    template_name = 'airwrite/home/home.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     q = self.request.GET.get('q')

    #     repo = DjangoModuleRepository()
    #     use_case = ListModulesUseCase(repo)
    #     modules = use_case.execute(ListModulesQuery(q=q))

    #     context.update({'modules': modules, 'title': 'Module List'})
    #     return context