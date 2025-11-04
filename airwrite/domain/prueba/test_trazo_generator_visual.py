# airwrite/domain/prueba/test_trazo_generator_visual.py
from airwrite.infrastructure.opencv.trazo_extractor import generar_trazo_desde_imagen
import matplotlib.pyplot as plt

def main():
    ruta = "media/letras/LETRA_A.png"
    print(f"Generando trazo desde: {ruta}")

    trazo = generar_trazo_desde_imagen(ruta, n_points=64, target_size=256)
    puntos = trazo.coordenadas  # ✅ usamos el nombre correcto

    print(f"Puntos generados: {len(puntos)}")
    print(puntos[:10])  # muestra algunos para verificar

    # --- Visualización con matplotlib ---
    x = [p[0] for p in puntos]
    y = [p[1] for p in puntos]

    plt.figure(figsize=(4, 4))
    plt.imshow(plt.imread(ruta))  # muestra la imagen original detrás
    plt.plot(x, y, 'ro-', linewidth=1.5, markersize=3)  # dibuja los puntos del trazo
    plt.title("Trazo generado para la letra A")
    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    main()


""" 
python -m airwrite.domain.prueba.test_trazo_generator_visual
"""