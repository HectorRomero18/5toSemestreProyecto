# test_validador.py
from airwrite.domain.entities.usuario import Usuario
from airwrite.domain.entities.letra import LetraEntity
from airwrite.domain.entities.trazo import Trazo
from airwrite.application.use_cases.validar_escritura import ValidadorEscrituraUseCase

def test_validador():
    # Crear usuario
    usuario = Usuario(nombre="John")

    # Crear letra de referencia con un trazo simple
    trazo_ref = Trazo(coordenadas=[(0, 0), (1, 1), (2, 2)])
    letra = LetraEntity(id=1, caracter="A", trazos=[trazo_ref])

    # Crear trazo simulado del usuario
    trazo_usuario = Trazo(coordenadas=[(0, 0), (1, 1.1), (2.1, 2)])

    # Instanciar el caso de uso
    validador = ValidadorEscrituraUseCase(usuario=usuario, umbral_similitud=0.7)

    # Ejecutar validación
    resultado = validador.ejecutar_validacion(letra, trazo_usuario)

    # Mostrar resultados
    print("Resultado de validación:")
    for key, value in resultado.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    test_validador()


""" 
python -m airwrite.domain.prueba.test_validador
"""

