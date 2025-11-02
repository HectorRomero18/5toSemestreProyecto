from django.urls import path
from airwrite.interfaces.django_views.numeros_tts_view import PlayNumberView

urlpatterns = [
     path('play/<str:number>/', PlayNumberView.as_view(), name='play_number'),
]
