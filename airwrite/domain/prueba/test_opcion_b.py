import cv2
import numpy as np
from airwrite.infrastructure.repositories.state import OpenCVCamera, CanvasState, CommandState
from airwrite.application.use_cases.drawing_loop import DrawingLoop, DrawingConfig, DrawingState
from airwrite.domain.entities.usuario import Usuario
from airwrite.domain.entities.letra import LetraEntity
from airwrite.domain.entities.trazo import Trazo
from airwrite.application.use_cases.validar_escritura import ValidadorEscrituraUseCase


def main():
    # ====== CONFIGURACIONES ======
    cam = OpenCVCamera(index=0)
    canvas = CanvasState()
    commands = CommandState()

    cfg = DrawingConfig(
        celeste_low=np.array([85, 100, 100]),
        celeste_high=np.array([100, 255, 255]),
        color_celeste=(255, 255, 0),
        color_amarillo=(0, 255, 255),
        color_rosa=(255, 0, 255),
        color_verde=(0, 255, 0),
        color_clear=(0, 0, 0),
        target_size=(480, 640)
    )
    state = DrawingState()
    drawing = DrawingLoop(cam, canvas, commands, cfg, state)

    # ====== VALIDACIÓN ======
    usuario = Usuario(nombre="John")
    validador = ValidadorEscrituraUseCase(usuario)

    trazo_ref = Trazo(coordenadas=[(50, 50), (150, 150)])
    letra_ref = LetraEntity(id=1, caracter="A", trazos=[trazo_ref])

    print("🎥 Cámara iniciada. Presiona 'v' para validar o 'q' para salir.\n")

    while True:
        drawing.step()
        frame = drawing.get_last_camera()
        lienzo = canvas.get()

        if frame is None or lienzo is None:
            continue

        combined = np.hstack((frame, lienzo))
        cv2.imshow("AirWrite - Opción B", combined)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

        elif key == ord('v'):
            # Por ahora usamos un trazo simulado hasta que captemos puntos reales del marcador
            trazo_usuario = Trazo(coordenadas=[(55, 55), (145, 145)])
            resultado = validador.ejecutar_validacion(letra_ref, trazo_usuario)

            print("\n🧾 RESULTADO DE VALIDACIÓN 🧾")
            print(f"Usuario: {resultado['usuario']}")
            print(f"Letra: {resultado['letra']}")
            print(f"Correcto: {'✅ Sí' if resultado['es_correcto'] else '❌ No'}")
            print(f"Similitud: {resultado['similitud']*100:.2f}%")
            print(f"Intentos: {resultado['intentos']}")
            print(f"Tiempo total letra: {resultado['tiempo_total_letra']:.2f} seg\n")

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
