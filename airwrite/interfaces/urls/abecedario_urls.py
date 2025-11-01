from django.urls import path
from airwrite.interfaces.django_views.abecedario_tts_view import PlayLetterView

urlpatterns = [
    path('letters/play/<str:letter>/', PlayLetterView.as_view(), name='play_letter'),
]
