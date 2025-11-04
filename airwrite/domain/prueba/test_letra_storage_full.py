from airwrite.infrastructure.storage.letra_storage import LetraStorage
from pprint import pprint

def main():
    storage = LetraStorage(carpeta_media="media")
    letras = storage.cargar_letras(generate_trazos=True, n_points=64)
    print("Total letras cargadas:", len(letras))
    sample = letras.get("A") or letras.get("1")
    if sample:
        print("Ejemplo:", sample.caracter, sample.imagen)
        print("Trazos guardados:", len(sample.trazos))
        if sample.trazos:
            print("Primeros 10 puntos:")
            pprint(sample.trazos[0].coordenadas[:10])

if __name__ == "__main__":
    main()
    
    
""" Para probar ejecutar
python -m airwrite.domain.prueba.test_letra_storage_full
"""