from django.http import StreamingHttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import cv2
import numpy as np
import time
import json

from django.views.decorators.http import require_POST
from airwrite.infrastructure.models.letra import Letra
from airwrite.infrastructure.models.numeros import Numero
from airwrite.infrastructure.models.silabas import Silaba
from airwrite.infrastructure.decoradores.decorador import requiere_desbloqueo

from airwrite.application.use_cases.drawing_loop import DrawingLoop, DrawingConfig, DrawingState
from airwrite.infrastructure.repositories.state import OpenCVCamera, CanvasState, CommandState
from airwrite.infrastructure.repositories.adapters import CameraAdapter, CanvasAdapter, CommandAdapter

from airwrite.domain.constants.xp_reward import DIFICULTADES, CATEGORIAS_LETRAS
import unicodedata
from airwrite.domain.services.evaluar_trazo import evaluar_trazo_por_contorno
from airwrite.domain.services.xp_reward_services import calcular_xp_ganado
from airwrite.domain.services.bloquear import esta_bloqueada
from airwrite.infrastructure.repositories.compra_letra import DjangoPerfilRepository
from airwrite.infrastructure.models.PerfilUsuario import PerfilUsuario

def quitar_tildes(texto: str) -> str:
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

CATEGORIAS_DICT = dict(CATEGORIAS_LETRAS)
DIFICULTADES_DICT = dict(DIFICULTADES)


_camera = OpenCVCamera(index=0)
_canvas_state = CanvasState()
_cmd_state = CommandState()

_cam_port = CameraAdapter(_camera)
_canvas_port = CanvasAdapter(_canvas_state)
_cmd_port = CommandAdapter(_cmd_state)

_cfg = DrawingConfig(
    celeste_low=(105, 150, 40),
    celeste_high=(130, 255, 150),
    # azul_low=(105, 150, 40),
    # azul_high=(130, 255, 150),
    # rojo_low=(0, 120, 70),
    # rojo_high=(10, 255, 255),
    color_celeste=(255, 113, 82),
    color_amarillo=(0, 0, 255),
    color_rosa=(128, 0, 255),
    color_verde=(0, 255, 36),
    color_uva=(150, 50, 150),
    color_menta=(212, 255, 127),
    color_clear=(29, 112, 246),
    target_size=(600, 800)  # Mejor calidad para trazos más suaves
)
_state = DrawingState()
_loop = DrawingLoop(_cam_port, _canvas_port, _cmd_port, _cfg, _state)


@requiere_desbloqueo
@login_required
def index(request, letra_id=None, numero_id=None, silaba_id=None, tipo='letra'):
    objeto = None

    # Si se pasa letra_id, obtiene una Letra
    if letra_id:
        objeto = get_object_or_404(Letra, id=letra_id)
        tipo = 'letra'

    # Si se pasa numero_id, obtiene un Número
    elif numero_id:
        objeto = get_object_or_404(Numero, id=numero_id)
        tipo = 'numero'

    elif silaba_id:
        objeto = get_object_or_404(Silaba, id=silaba_id)
        tipo = 'silaba'

    # Enable tracing mode for manual drawing control
    if objeto is not None:
        _loop.enable_tracing_mode()
        _state.drawing_active = False  # Dibujo inactivo por defecto

        from airwrite.infrastructure.opencv.trazo_extractor import reiniciar_lienzo
        texto = objeto.nombre.split()[-1].upper()[-2:] if tipo == 'silaba' else objeto.nombre[-1].upper()
        frame_shape = (600, 800, 3)  # Mejor calidad para trazos más suaves
        base, modelo = reiniciar_lienzo(frame_shape, texto)
        _state.base_canvas = base
        _state.modelo_gray = modelo
        _state.current_texto = texto

    if objeto:
        print(f"Letra cargada: {objeto.nombre}")
    context = {
        'objeto': objeto,  # Puede ser Letra o Número
        'tipo': tipo,
    }
    return render(request, 'airwrite/index.html', context)


def _lazy_start():
    _cam_port.start()


def video_feed_cam(request):
    def gen():
        while True:
            _lazy_start()
            _loop.step()
            frame = _loop.get_last_camera()
            if frame is None:
                time.sleep(0.01)
                continue
            ret, jpeg = cv2.imencode('.jpg', frame)
            if not ret:
                continue
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
    return StreamingHttpResponse(gen(), content_type='multipart/x-mixed-replace; boundary=frame')

def video_feed_canvas(request, tipo, objeto_id):
    """
    Muestra en streaming la imagen de una letra o número centrada en el lienzo.
    tipo: 'letra' o 'numero'
    objeto_id: id del objeto en su respectivo modelo
    """
    perfil = getattr(request.user, 'perfilusuario', None)
    no_bloqueadas = ["Letra A", "Letra B", "Letra C"]
    # Validar tipo y obtener objeto
    if tipo == 'numero':
        objeto = get_object_or_404(Numero, id=objeto_id)
        desbloqueada = True  # Números siempre desbloqueados
    elif tipo == 'letra':
        objeto = get_object_or_404(Letra, id=objeto_id)
        desbloqueada = not esta_bloqueada(request.user, objeto.nombre)

    elif tipo == 'silaba':
        objeto = get_object_or_404(Silaba, id=objeto_id)
        desbloqueada = (perfil and objeto in perfil.silabas_desbloqueadas.all()) or objeto.nombre in ["Silaba ba", "Silaba be", "Silaba ca"]
    else:
        raise ValueError("Tipo inválido")

    texto = DIFICULTADES_DICT.get(objeto.dificultad, '')
    texto_sin_tilde = quitar_tildes(texto)

    def gen():
        while True:
            _lazy_start()
            _loop.step()
            canvas = _canvas_port.get()

            if canvas is None:
                time.sleep(0.01)
                continue

            # Usar base_canvas si existe, sino crear lienzo base con cuadrícula
            if _state.base_canvas is not None:
                blank_canvas = _state.base_canvas.copy()
            else:
                blank_canvas = np.ones(canvas.shape, dtype=np.uint8) * 200
                grid_size = 17
                blank_canvas[::grid_size, :] = 150
                blank_canvas[:, ::grid_size] = 150

            # Imagen desbloqueada o permitida

            if (desbloqueada):
                objeto_nombre = objeto.nombre

                if objeto_nombre is None:
                    print(f"Error al leer el objeto con ID {objeto.id}.")
                    continue


                # --- Texto de información ---
                color_dif = {
                    'Facil': (0, 255, 0),
                    'Media': (211, 0, 148),
                    'Dificil': (0, 0, 255)
                }.get(texto_sin_tilde, (255, 255, 255))

                # Texto principal (más abajo)
                cv2.putText(blank_canvas, f"{objeto.nombre}", (20, 200),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (50, 50, 50), 3)

                # Texto de dificultad (posición fija a la derecha)
                cv2.putText(blank_canvas, f"Dificultad: {texto_sin_tilde}", (690, 200),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, color_dif, 3)

                if tipo == 'letra':
                    if objeto.categoria == 'V':
                        cv2.putText(blank_canvas, f"{CATEGORIAS_DICT[objeto.categoria]}",
                                    (20, 250), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
                    elif objeto.categoria == 'C':
                        cv2.putText(blank_canvas, f"{CATEGORIAS_DICT[objeto.categoria]}",
                                (20, 250), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 3)

            # Copiar los trazos del usuario sobre el lienzo base
            bg_mask = (canvas == 200).all(axis=2)
            grid_mask = (canvas == 150).all(axis=2)
            drawing_mask = ~(bg_mask | grid_mask)
            blank_canvas[drawing_mask] = canvas[drawing_mask]


            # Convertir a JPEG
            ret, jpeg = cv2.imencode('.jpg', blank_canvas)
            if not ret:
                continue

            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' +
                   jpeg.tobytes() + b'\r\n')

    return StreamingHttpResponse(gen(), content_type='multipart/x-mixed-replace; boundary=frame')


def set_voice_command(text: str | None):
    _cmd_port.set(text)


def clear_canvas(request):
    _cmd_port.set("limpiar pantalla")
    return JsonResponse({"status": "ok"})


@require_POST
def set_color(request):
    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "error": "invalid_payload"}, status=400)
    color = payload.get("color")
    if not color:
        return JsonResponse({"status": "error", "error": "color_required"}, status=400)
    if _loop.set_color(color):
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error", "error": "color_invalid"}, status=400)


@require_POST
def set_grosor(request):
    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "error": "invalid_payload"}, status=400)
    grosor = payload.get("grosor")
    if not grosor:
        return JsonResponse({"status": "error", "error": "grosor_required"}, status=400)

    # Intentar aplicar cambio directamente en _loop si existe una API
    ok = False
    try:
        if hasattr(_loop, "set_thickness"):
            ok = _loop.set_thickness(grosor)
        elif hasattr(_loop, "set_brush_size"):
            ok = _loop.set_brush_size(grosor)
        elif hasattr(_loop, "set_grosor"):
            ok = _loop.set_grosor(grosor)
        else:
            # Fallback: enviar comando de voz al loop (si el loop procesa comandos de texto)
            _cmd_port.set(f"grosor {grosor}")
            ok = True
    except Exception:
        ok = False

    if ok:
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error", "error": "grosor_invalid"}, status=400)


@require_POST
def toggle_drawing(request):
    """Endpoint to toggle drawing on/off in tracing mode"""
    try:
        _loop.toggle_drawing()
        return JsonResponse({"status": "ok"})
    except Exception as e:
        return JsonResponse({"status": "error", "error": str(e)}, status=500)


@require_POST
def validar_trazo(request):
    """Evaluar la precisión del trazo dibujado"""
    if _state.base_canvas is None or _state.modelo_gray is None:
        return JsonResponse({"status": "error", "error": "no_modelo"})

    try:
        data = json.loads(request.body.decode("utf-8") or "{}")
        puntos = data.get("puntos", [])
    except json.JSONDecodeError:
        puntos = []

    if not puntos:
        # Fallback: intentar detectar trazos desde la cámara (método original)
        canvas = _canvas_port.get()
        if canvas is None:
            return JsonResponse({"status": "error", "error": "no_canvas"})

        # Crear imAux: base_canvas con trazos superpuestos
        imAux = _state.base_canvas.copy()
        bg_mask = (canvas == 200).all(axis=2)
        grid_mask = (canvas == 150).all(axis=2)
        drawing_mask = ~(bg_mask | grid_mask)

        print(f"Drawing mask sum: {drawing_mask.sum()}")  # Debug

        # Verificar si hay algún trazo dibujado
        if not drawing_mask.any():
            return JsonResponse({"status": "error", "error": "No se encontró ningún trazo para verificar."})

        imAux[drawing_mask] = canvas[drawing_mask]
    else:
        # Usar puntos del mouse/touch para crear el trazo
        imAux = _state.base_canvas.copy()
        if puntos:
            # Convertir puntos a coordenadas del canvas
            # El canvas es de 600x1080, pero los puntos vienen del frontend que puede tener diferente tamaño
            # Asumimos que los puntos están en la escala correcta o los escalamos
            canvas_h, canvas_w = imAux.shape[:2]

            # Dibujar líneas entre puntos consecutivos
            for i in range(len(puntos) - 1):
                p1 = tuple(puntos[i])
                p2 = tuple(puntos[i + 1])
                # Asegurarse de que las coordenadas estén dentro del canvas
                p1 = (max(0, min(p1[0], canvas_w - 1)), max(0, min(p1[1], canvas_h - 1)))
                p2 = (max(0, min(p2[0], canvas_w - 1)), max(0, min(p2[1], canvas_h - 1)))
                cv2.line(imAux, p1, p2, (255, 113, 82), 3, cv2.LINE_AA)

    score, overlay = evaluar_trazo_por_contorno(imAux, _state.base_canvas, _state.modelo_gray)
    print(f"Score: {score}, Puntos: {len(puntos) if puntos else 'camera'}")  # Debug

    xp_ganado = 0
    nuevo_xp = 0

    if score >= 70:
        # Obtener tipo y objeto_id del request
        data = json.loads(request.body.decode("utf-8") or "{}")
        tipo = data.get("tipo")
        objeto_id = data.get("objeto_id")

        if tipo and objeto_id:
            # Verificar si ya se completó este objeto
            completados_key = f'completados_{tipo}'
            completados = request.session.get(completados_key, [])
            objeto_key = f"{tipo}_{objeto_id}"

            if objeto_key in completados:
                # Ya completado, no sumar XP
                xp_ganado = 0
                nuevo_xp = 0
            else:
                # Obtener el objeto
                if tipo == 'letra':
                    objeto = get_object_or_404(Letra, id=objeto_id)
                elif tipo == 'numero':
                    objeto = get_object_or_404(Numero, id=objeto_id)
                elif tipo == 'silaba':
                    objeto = get_object_or_404(Silaba, id=objeto_id)
                else:
                    return JsonResponse({"status": "error", "error": "tipo_invalido"})

                # Calcular XP ganado
                xp_ganado = calcular_xp_ganado(objeto.dificultad)

                # Obtener perfil model y sumar XP
                perfil_model = PerfilUsuario.objects.get(user_id=request.user.id)
                perfil_model.xp += xp_ganado
                # Agregar a letras practicadas si es letra
                if tipo == 'letra':
                    perfil_model.letras_practicadas.add(objeto)
                perfil_model.save()
                nuevo_xp = perfil_model.xp

                # Marcar como completado
                completados.append(objeto_key)
                request.session[completados_key] = completados
        else:
            xp_ganado = 0
            nuevo_xp = 0
    else:
        xp_ganado = 0
        nuevo_xp = 0

    return JsonResponse({"status": "ok", "score": score, "xp_ganado": xp_ganado, "nuevo_xp": nuevo_xp})
