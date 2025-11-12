"""
Prueba integral del módulo trazo_extractor dentro del proyecto Django.
Permite verificar que la cámara se inicie, se detecte color, 
y se pueda dibujar con la tecla 'A' como en la versión original.
"""

from airwrite.infrastructure.opencv.trazo_extractor import iniciar_practica

if __name__ == "__main__":
    print("=== PRUEBA INTEGRAL DE TRAZO EXTRACTOR ===")
    print("🟢 Iniciando cámara...")
    print("Usa la tecla 'A' para empezar/detener dibujo.")
    print("Usa la barra espaciadora para reiniciar el lienzo.")
    print("Usa 'E' para evaluar tu trazo y 'ESC' para salir.\n")

    try:
        iniciar_practica("letras")
    except Exception as e:
        print("❌ Error al ejecutar la prueba:")
        print(e)


""" Para probar ejecutar
python -m airwrite.domain.prueba.test_captura_trazo

"""