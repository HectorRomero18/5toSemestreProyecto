from django.urls import path
from django.contrib.auth import views as auth_views
from airwrite.interfaces.django_views.auth import LoginView, CustomLogoutView
from airwrite.interfaces.django_views.home import ModuleListView as HomeModuleListView
from airwrite.interfaces.django_views.abecedario import AbecedarioListView
from airwrite.interfaces.django_views.tiendaXp import TiendaXpListView as TiendaXpModuleListView
from airwrite.interfaces.django_views.silaba import ModuleListView as SilabaModuleListView
from airwrite.interfaces.django_views.trazos import index, video_feed_cam, video_feed_canvas, clear_canvas, set_color, set_grosor
from airwrite.interfaces.django_views.compra_letra import comprar_letra
#from core.views.login import login_view

urlpatterns = [
    # Rutas actuales
    # path('', index, name='home'),
    # path('', login_view, name='login'),   # Página inicial
    # path('home/', ModuleListView.as_view(), name='home'),

    # mostrar login al abrir la raíz
    path('', LoginView.as_view(), name='login'),
    path('login/', LoginView.as_view(), name='login'), 

    path('home/', HomeModuleListView.as_view(), name='home'),
    # logout (usa POST o LogoutView)
    path('logout/', CustomLogoutView.as_view(), name='logout'),


    path('trazos/', index, name='trazos'),
    path('video/cam/', video_feed_cam, name='video_feed_cam'),
    path('video/canvas/', video_feed_canvas, name='video_feed_canvas'),
    path('clear/', clear_canvas, name='clear_canvas'),
    path('set_grosor/', set_grosor, name='set_grosor'),

    path('color/', set_color, name='set_color'),

    path('abecedario/', AbecedarioListView.as_view(), name='abecedario'),
    path('tienda/', TiendaXpModuleListView.as_view(), name='tienda'),
    path('silaba/', SilabaModuleListView.as_view(), name='silaba'),
    path('tiendaXp/comprar/', comprar_letra, name='comprar_letra'),
]