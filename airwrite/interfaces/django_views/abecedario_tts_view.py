from django.http import FileResponse, Http404
from django.views import View
from airwrite.domain.services.text_to_speech_service import TextToSpeechService
import os

class PlayLetterView(View):
    def get(self, request, letter):
        try:
            tts_service = TextToSpeechService()
            audio_path = tts_service.synthesize_letter(letter)
            if not os.path.exists(audio_path):
                raise Http404("Audio no encontrado")
            return FileResponse(open(audio_path, "rb"), content_type="audio/wav")
        except Exception as e:
            return Http404(f"Error generando audio: {e}")
