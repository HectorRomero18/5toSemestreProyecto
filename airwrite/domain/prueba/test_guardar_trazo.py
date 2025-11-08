import cv2
from airwrite.infrastructure.repositories.state import CanvasState
from airwrite.infrastructure.repositories.canvas_with_trace import CanvasAdapterWithTrace

def test_guardar_trazo():
    # Inicializa el canvas
    state = CanvasState()
    canvas = CanvasAdapterWithTrace(state)

    # Simula dibujo
    shape = (400, 400, 3)
    canvas.ensure_shape(shape)

    # Simula puntos dibujados
    points = [(50, 50), (60, 60), (80, 100), (150, 200), (200, 250)]
    for i in range(1, len(points)):
        canvas.draw_line(points[i-1], points[i], (0, 0, 255), 2)

    # Exportar trazo
    filename = canvas.export_trace_to_file("trazo_prueba.json")
    print(f"✅ Trazo exportado correctamente en {filename}")

    # Mostrar imagen
    img = canvas.get()
    cv2.imshow("Canvas de Prueba", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    test_guardar_trazo()

""""
python -m airwrite.domain.prueba.test_guardar_trazo  
"""