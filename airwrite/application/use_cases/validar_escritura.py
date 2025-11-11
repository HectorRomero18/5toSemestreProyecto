from airwrite.domain.entities.usuario import Usuario
from airwrite.domain.entities.letra import LetraEntity
from airwrite.domain.entities.trazo import Trazo
from airwrite.domain.services.validar_trazo import ValidarTrazo
from airwrite.domain.services.estadisticas import EstadisticasService
from typing import Dict, Any


""" Caso de uso que valida el trazo de un usuario comparándolo con la letra de referencia """
class ValidadorEscrituraUseCase:
    def __init__(self, usuario: Usuario, umbral_similitud: float = 0.60):
        self.usuario = usuario
        self.validador = ValidarTrazo(umbral_similitud=umbral_similitud)
        self.estadisticas = EstadisticasService(usuario)

    def ejecutar_validacion(self, letra: LetraEntity, trazo_usuario: Trazo) -> Dict[str, Any]:
        """
        Compara el trazo del usuario con la referencia de la letra y actualiza estadísticas.

        Retorna un diccionario con los resultados principales.
        """

        # Validaciones básicas
        if letra is None:
            raise ValueError("El parámetro 'letra' no puede ser None.")
        if not letra.trazos:
            raise ValueError(f"La letra '{letra.caracter}' no tiene trazos de referencia definidos.")

        # Tomar el trazo de referencia principal
        trazo_referencia = letra.trazos[0]

        # Ejecutar validación
        resultado = self.validador.validar_trazo(trazo_referencia, trazo_usuario)

        # Registrar resultado en estadísticas
        try:
            self.estadisticas.registrar_resultado(self.usuario, letra, resultado)
        except AttributeError:
            # Si el servicio de estadísticas tiene una firma distinta, evitamos que rompa el flujo
            pass

        # Intentos (manejo seguro)
        try:
            intentos = self.estadisticas.obtener_intentos(self.usuario, letra)
        except Exception:
            intentos = 0

        # Retornar datos resumidos
        return {
            "usuario": getattr(self.usuario, "nombre", "Desconocido"),
            "letra": getattr(letra, "caracter", None),
            "es_correcto": getattr(resultado, "es_correcto", False),
            "similitud": round(getattr(resultado, "similitud", 0.0), 3),
            "intentos": intentos,
            "tiempo_total_letra": round(letra.tiempo_total(), 3) if hasattr(letra, "tiempo_total") else None,
        }
