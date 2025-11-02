# # airwrite/domain/services/text_to_speech_service_numbers.py
# from google.cloud import texttospeech
# import os

# class TextToSpeechNumbersService:
#     """
#     Servicio TTS separado para números.
#     Devuelve bytes WAV (LINEAR16).
#     """

#     def __init__(self):
#         cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
#         if not cred_path:
#             raise Exception("Debes definir GOOGLE_APPLICATION_CREDENTIALS en las variables de entorno")
#         # inicializa el cliente (usar ADC)
#         self.client = texttospeech.TextToSpeechClient()

#     def synthesize_number(self, number_text: str, language_code: str = "es-US", voice_name: str = "es-US-Wavenet-B"):
#         """
#         number_text: texto a decir, p. ej. "Número 1" o "Uno".
#         Retorna: bytes del audio en LINEAR16 (wav).
#         """
#         if not number_text:
#             raise ValueError("Texto vacío")

#         synthesis_input = texttospeech.SynthesisInput(text=number_text)

#         voice = texttospeech.VoiceSelectionParams(
#             language_code=language_code,
#             name=voice_name,
#             # ssml_gender puede omitirse o usarse
#         )

#         audio_config = texttospeech.AudioConfig(
#             audio_encoding=texttospeech.AudioEncoding.LINEAR16
#         )

#         response = self.client.synthesize_speech(
#             input=synthesis_input,
#             voice=voice,
#             audio_config=audio_config
#         )

#         return response.audio_content
