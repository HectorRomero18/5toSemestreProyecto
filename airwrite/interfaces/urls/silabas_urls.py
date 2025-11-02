from django.urls import path
from airwrite.interfaces.django_views.silabas_tts_view import PlaySilabaView

urlpatterns = [
    path('play/<str:silaba>/', PlaySilabaView.as_view(), name='play_silaba'),
]
