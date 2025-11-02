from airwrite.domain.services.text_to_speech_service import TextToSpeechService

class PlayLetterUseCase:
    def __init__(self, tts_service: TextToSpeechService):
        self.tts_service = tts_service

    def execute(self, letter: str) -> bytes:
        return self.tts_service.synthesize_letter(letter)
