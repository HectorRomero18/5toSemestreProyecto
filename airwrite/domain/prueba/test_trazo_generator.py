# airwrite/domain/prueba/test_trazo_generator.py
from airwrite.infrastructure.opencv.trazo_extractor import generar_trazo_desde_imagen
from pprint import pprint

def main():
    ruta = "media/letras/LETRA_A.png"  # ajusta según tu archivo
    print("Generando trazo desde:", ruta)
    trazo = generar_trazo_desde_imagen(ruta, n_points=64, target_size=256)
    print("Puntos generados:", len(trazo.coordenadas))
    pprint(trazo.coordenadas[:10])

if __name__ == "__main__":
    main()


""" Para probar ejecutar
python -m airwrite.domain.prueba.test_trazo_generator

"""