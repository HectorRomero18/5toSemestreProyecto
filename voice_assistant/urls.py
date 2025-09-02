from django.urls import path
from voice_assistant.views.voice_assis import transcribir_audio

urlpatterns = [
    path("transcribir-api/", transcribir_audio, name="transcribir_audio_api"),
]
