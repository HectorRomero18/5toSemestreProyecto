from airwrite.domain.entities.usuario import Usuario
from airwrite.domain.entities.letra import LetraEntity
from airwrite.domain.entities.trazo import Trazo
from airwrite.application.use_cases.validar_escritura import ValidadorEscrituraUseCase
import random

def test_validador_multiple():
    # Crear un usuario simulado
    usuario = Usuario(nombre="John")

    # Instanciar el caso de uso con el usuario
    validador = ValidadorEscrituraUseCase(usuario, umbral_similitud=0.7)

    # Simulamos varias letras de referencia y sus trazos (ahora con id)
    letras = [
        LetraEntity(id=1, caracter="A", trazos=[Trazo([(0, 0), (1, 1), (2, 2)])]),
        LetraEntity(id=2, caracter="B", trazos=[Trazo([(0, 0), (0, 1), (0, 2)])]),
        LetraEntity(id=3, caracter="C", trazos=[Trazo([(2, 0), (1, 1), (0, 2)])]),
    ]

    print(f"=== Simulación de validación para el usuario '{usuario.nombre}' ===\n")

    resultados = []

    for letra in letras:
        # Simulamos ligeras variaciones en el trazo del usuario
        trazo_usuario = Trazo([
            (x + random.uniform(-0.3, 0.3), y + random.uniform(-0.3, 0.3))
            for x, y in letra.trazos[0].coordenadas
        ])

        # Ejecutar la validación del caso de uso
        resultado = validador.ejecutar_validacion( letra, trazo_usuario)

        # Mostrar el resultado individual
        print(f"Letra {resultado['letra']}: Similitud {resultado['similitud']}% | Correcto: {resultado['es_correcto']}")

        # Guardar solo el valor de similitud para calcular promedio
        resultados.append(resultado["similitud"])

    # Mostrar resumen general
    promedio = sum(resultados) / len(resultados)
    print(f"\nPromedio general de similitud: {round(promedio, 2)}%")

if __name__ == "__main__":
    test_validador_multiple()
