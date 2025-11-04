import sys
from pathlib import Path

# Agrega la raíz del proyecto al path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from infrastructure.storage.letra_storage import LetraStorage

def main():
    print("🔍 Iniciando prueba de carga de letras...\n")

    # Crear instancia del almacenamiento de letras
    storage = LetraStorage(carpeta_media="media")

    # Cargar todas las letras desde las subcarpetas (letra, numero, etc.)
    try:
        letras = storage.cargar_letras()
        print(f"✅ Se cargaron {len(letras)} letras correctamente.\n")
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        return

    # Mostrar las letras encontradas
    print("📄 Letras encontradas:")
    for caracter, letra in letras.items():
        print(f"  - {caracter} → {letra}")

    # Probar obtener una letra específica
    print("\n🧩 Probando obtención individual:")
    try:
        letra_a = storage.obtener_letra("A")
        print(f"✅ Letra 'A' encontrada: {letra_a}")
    except FileNotFoundError:
        print("⚠️ La letra 'A' no fue encontrada en las carpetas.")

    # Mostrar letras disponibles en caché
    print("\n💾 Letras almacenadas en caché:")
    print(storage.listar_letras_disponibles())

if __name__ == "__main__":
    main()


""" Para probar ejecutar
python -m airwrite.domain.prueba.test_trazo_storage

"""