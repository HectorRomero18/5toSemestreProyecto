from google.cloud import texttospeech
import os

class TextToSpeechService:
    def __init__(self):
        # Esto asegura que el cliente encuentre tu JSON
        cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        if not cred_path:
            raise Exception("Debes definir GOOGLE_APPLICATION_CREDENTIALS")
        self.client = texttospeech.TextToSpeechClient()

    def synthesize_letter(self, letter: str, output_path: str = "media/temp_audio.wav"):
        synthesis_input = texttospeech.SynthesisInput(text=letter)
        
        # Configuración de voz (español neutro)
        voice = texttospeech.VoiceSelectionParams(
           language_code="es-US",  # Cambia a "en-US" para inglés
           name="es-US-Wavenet-B", # Especifica una voz concreta
           ssml_gender=texttospeech.SsmlVoiceGender.FEMALE

        )
        
        # Configuración de audio
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16
        )
        
        response = self.client.synthesize_speech(
            input=synthesis_input, 
            voice=voice, 
            audio_config=audio_config
        )
        
        # Guardar archivo
        with open(output_path, "wb") as out:
            out.write(response.audio_content)
        return output_path
