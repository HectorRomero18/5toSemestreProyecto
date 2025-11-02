from google.cloud import texttospeech
import os

class TextToSpeechService:
    def __init__(self):
        cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        if not cred_path:
            raise Exception("Debes definir GOOGLE_APPLICATION_CREDENTIALS")
        self.client = texttospeech.TextToSpeechClient()

    def synthesize_text(self, text: str, output_path: str = "media/temp_audio.wav"):
        """
        Método genérico para sintetizar texto (letras, números, palabras, etc.)
        """
        synthesis_input = texttospeech.SynthesisInput(text=text)

        voice = texttospeech.VoiceSelectionParams(
            language_code="es-US",
            name="es-US-Wavenet-B",
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16
        )

        response = self.client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )

        with open(output_path, "wb") as out:
            out.write(response.audio_content)

        return output_path

    # Mantenemos compatibilidad con el método anterior
    def synthesize_letter(self, letter: str, output_path: str = "media/temp_audio.wav"):
        return self.synthesize_text(letter, output_path)
