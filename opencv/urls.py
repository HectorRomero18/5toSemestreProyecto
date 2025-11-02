"""
URL configuration for opencv project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
# from django.http import HttpResponse


urlpatterns = [
    # path('', lambda request: HttpResponse("Bienvenido a Django 🚀"), name='home'),
    path('admin/', admin.site.urls),
    # Rutas migradas a airwrite (hexagonal interfaces)
    path('', include('airwrite.interfaces.urls.urls_core')),
    path('voice/', include('airwrite.interfaces.urls.urls_voice')),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # produce /accounts/logout/ con name='logout'
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('abecedario/', include('airwrite.interfaces.urls.abecedario_urls')),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

