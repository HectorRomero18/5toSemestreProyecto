from airwrite.domain.entities.usuario import Usuario
from airwrite.domain.entities.letra import LetraEntity
from airwrite.domain.entities.trazo import Trazo
from airwrite.application.use_cases.validar_escritura import ValidadorEscrituraUseCase

def test_validador():
    # 1️⃣ Crear usuario de prueba
    usuario = Usuario(nombre="John")

    # 2️⃣ Crear instancia del validador pasando el usuario
    validador = ValidadorEscrituraUseCase(usuario=usuario, umbral_similitud=0.7)

    # 3️⃣ Crear letra y trazo de referencia
    trazo_ref = Trazo(coordenadas=[(0, 0), (1, 1), (2, 2)])
    letra = LetraEntity(id=1, caracter="A", trazos=[trazo_ref])

    # 4️⃣ Simular trazo del usuario
    trazo_usuario = Trazo(coordenadas=[(0, 0), (1, 1.1), (2.1, 2)])

    # 5️⃣ Ejecutar validación
    resultado = validador.ejecutar_validacion(letra, trazo_usuario)

    # 6️⃣ Mostrar resultado
    print("Resultado de validación:")
    print(f"Usuario: {resultado['usuario']}")
    print(f"Letra: {resultado['letra']}")
    print(f"Es correcto: {resultado['es_correcto']}")
    print(f"Similitud: {resultado['similitud']}")
    print(f"Intentos: {resultado['intentos']}")
    print(f"Tiempo total letra: {resultado['tiempo_total_letra']}")

if __name__ == "__main__":
    test_validador()


""" 
python -m airwrite.domain.prueba.test_validador
"""

