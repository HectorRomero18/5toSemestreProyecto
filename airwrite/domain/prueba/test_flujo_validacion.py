import json
from airwrite.infrastructure.repositories.canvas_with_trace import CanvasAdapterWithTrace
from airwrite.infrastructure.repositories.state import CanvasState
from airwrite.domain.entities.usuario import Usuario
from airwrite.domain.entities.trazo import Trazo
from airwrite.domain.entities.letra import LetraEntity
from airwrite.application.use_cases.validar_escritura import ValidadorEscrituraUseCase

# -----------------------------------------------------------
# Simulación: el usuario dibuja una letra y se compara con la de referencia
# -----------------------------------------------------------

def test_flujo_validacion():
    # 1️⃣ Simulamos que ya hay un trazo exportado por el canvas
    with open("trazo_prueba.json", "r", encoding="utf-8") as f:
        datos_trazo = json.load(f)

    # 2️⃣ Creamos el usuario
    usuario = Usuario(nombre=datos_trazo.get("usuario", "Anonimo"))

    # 3️⃣ Creamos el trazo del usuario (desde los puntos exportados)
    puntos_usuario = datos_trazo["trazo"]
    trazo_usuario = Trazo(puntos_usuario)

    # 4️⃣ Cargamos o simulamos el trazo de referencia de la letra "A"
    # Aquí puedes usar un archivo real o un trazo precargado
    trazo_referencia = Trazo([
        (40, 200), (60, 100), (80, 50), (100, 100), (120, 200)
    ])
    letra_ref = LetraEntity(id=1,caracter="A", trazos=[trazo_referencia])

    # 5️⃣ Ejecutamos la validación
    validador = ValidadorEscrituraUseCase(usuario)
    resultado = validador.ejecutar_validacion(letra_ref, trazo_usuario)

    # 6️⃣ Mostramos resultados
    print("\n🧾 RESULTADO DE VALIDACIÓN 🧾")
    print(f"Usuario: {resultado['usuario']}")
    print(f"Letra: {resultado['letra']}")
    print(f"Correcto: {'✅ Sí' if resultado['es_correcto'] else '❌ No'}")
    print(f"Similitud: {resultado['similitud'] * 100:.1f}%")
    print(f"Intentos: {resultado['intentos']}")
    print(f"Tiempo total letra: {resultado['tiempo_total_letra']} seg\n")


if __name__ == "__main__":
    test_flujo_validacion()