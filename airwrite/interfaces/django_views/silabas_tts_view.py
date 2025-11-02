from django.http import FileResponse, Http404
from django.views import View
from airwrite.domain.services.text_to_speech_service import TextToSpeechService
import os

class PlaySilabaView(View):
    def get(self, request, silaba):
        try:
            tts_service = TextToSpeechService()
            texto = f"Sílaba {silaba}"
            audio_path = tts_service.synthesize_text(texto)
            if not os.path.exists(audio_path):
                raise Http404("Audio no encontrado")
            return FileResponse(open(audio_path, "rb"), content_type="audio/wav")
        except Exception as e:
            raise Http404(f"Error generando audio: {e}")
