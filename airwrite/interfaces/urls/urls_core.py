from django.urls import path
from django.contrib.auth import views as auth_views
from airwrite.interfaces.django_views.auth import LoginView, CustomLogoutView
from airwrite.interfaces.django_views.home import ModuleListView
from airwrite.interfaces.django_views.trazos import index, video_feed_cam, video_feed_canvas, clear_canvas
#from core.views.login import login_view

urlpatterns = [
    # Rutas actuales
    # path('', index, name='home'),
    # path('', login_view, name='login'),   # Página inicial
    # path('home/', ModuleListView.as_view(), name='home'),

    # mostrar login al abrir la raíz
    path('', LoginView.as_view(), name='login'),
    path('login/', LoginView.as_view(), name='login'), 

    path('home/', ModuleListView.as_view(), name='home'),
    # logout (usa POST o LogoutView)
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    
    path('trazos/', index, name='trazos'),
    path('video/cam/', video_feed_cam, name='video_feed_cam'),
    path('video/canvas/', video_feed_canvas, name='video_feed_canvas'),
    path('clear/', clear_canvas, name='clear_canvas'),

    
]