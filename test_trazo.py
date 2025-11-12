from airwrite.infrastructure.opencv.trazo_extractor import generar_trazo_desde_imagen

# Prueba con la letra Z
path_z = "media/letras/letra_Z.png"  # Ajusta la ruta según tu estructura
try:
    trazo_z = generar_trazo_desde_imagen(path_z, n_points=64, target_size=256)
    print(f"Coordenadas de la letra Z: {trazo_z.coordenadas}")
    print(f"Número de puntos: {len(trazo_z.coordenadas)}")
except Exception as e:
    print(f"Error: {e}")

# Para verificar visualmente, dibuja los puntos
try:
    import matplotlib.pyplot as plt
    if 'trazo_z' in locals():
        coords = trazo_z.coordenadas
        x = [p[0] for p in coords]
        y = [p[1] for p in coords]
        plt.figure(figsize=(6,6))
        plt.plot(x, y, 'o-', markersize=3)
        plt.title("Trazo de la letra Z")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.axis('equal')
        plt.grid(True)
        plt.savefig("trazo_z.png")
        print("Gráfico guardado en trazo_z.png")
        plt.close()
except ImportError:
    print("Matplotlib no disponible, imprimiendo puntos:")
    if 'trazo_z' in locals():
        coords = trazo_z.coordenadas
        print(f"Primeros 10 puntos: {coords[:10]}")
        print(f"Últimos 10 puntos: {coords[-10:]}")