import subprocess
from core.views.trazos import comando_voz
import tempfile
import os
import whisper
from io import BytesIO
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Forzar ruta de ffmpeg
ffmpeg_path = r"C:\Users\Jorge\Downloads\ffmpeg-2025-09-01-git-3ea6c2fe25-full_build\bin"
os.environ["PATH"] += os.pathsep + ffmpeg_path



# Cargar modelo
model = whisper.load_model("base")


def convertir_a_wav16k(src_path: str) -> str:
    wav_path = src_path + ".wav"
    cmd = [
        "ffmpeg", "-y", "-i", src_path,
        "-ar", "16000", "-ac", "1",
        "-vn", "-sn", "-dn",
        wav_path
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    return wav_path 


@csrf_exempt
def transcribir_audio(request):
    try:
        if request.method == "POST" and request.FILES.get("audio"):
            audio_file = request.FILES["audio"]
            audio_bytes = BytesIO(audio_file.read())

            # Archivo temporal seguro
            with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as tmp_file:
                tmp_file.write(audio_bytes.getbuffer())
                tmp_path = tmp_file.name
            wav_path = convertir_a_wav16k(tmp_path)

            # Transcribir
            result = model.transcribe(
                wav_path,
                language="es",
                initial_prompt="Comandos: rosa, verde, celeste, amarillo",
                temperature=0.0,
                condition_on_previous_text=False,
                fp16=False
)
            comando = result["text"].lower()

            # Borrar temporal
            os.remove(tmp_path)
            os.remove(wav_path)

            comando_voz["valor"] = comando

            return JsonResponse({"comando": comando})

        return JsonResponse({"error": "Método no permitido"}, status=405)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
