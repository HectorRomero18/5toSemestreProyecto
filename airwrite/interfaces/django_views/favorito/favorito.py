# # Vistas de favoritos
# from django.views.generic import TemplateView

# from airwrite.application.use_cases.favorito.favorito_use_case import (
#      ListFavoritosQuery,
#      ListFavoritosUseCase,
#      AddFavoritoUseCase,
#      DeleteFavoritoUseCase,
#      ExistsFavoritoUseCase,
#      ExistsFavoritoQuery
    
# )
# from airwrite.infrastructure.repositories.favorito.favorito_repository import (
#     DjangoFavoritoRepository
# )

# from django.contrib.auth.mixins import LoginRequiredMixin


# DIFICULTADES_DICT = dict(DIFICULTADES)
# class FavoritoListView(LoginRequiredMixin, TemplateView):
#     template_name = 'airwrite/modules/favorito.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         q = self.request.GET.get('q')

#         repo = DjangoFavoritoRepository()
#         use_case = ListFavoritosUseCase(repo=repo)
#         user = self.request.user

#         modules = use_case.execute(ListFavoritosQuery(q=q))
        
#         # Convertir cada LetraEntity a dict
#         modules_serializable = []

#         for m in modules:
#             caracter_real = m.caracter[-1]  # toma solo la letra al final
#             # print("Caracter real:", caracter_real)

#             modules_serializable.append({
#                 'letter': m.caracter,
#                 'categoria': getattr(m, 'categoria', ''),
#                 'dificultad': DIFICULTADES_DICT.get(m.dificultad, ''),
#                 'price': getattr(m, 'price', 100),
#                 'simbolo': m.caracter[-1]  # para mostrar solo la letra
#             })


#         perfil = getattr(user, 'perfilusuario', None)
#         user_xp = perfil.xp if perfil else 0

#         context.update({
#             'modules': modules_serializable,
#             'title': 'Module List',
#             'user': user,
#             'user_xp': user_xp
#         })
#         return context
