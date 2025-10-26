from airwrite.domain.constants import XP_POR_DIFICULTAD

def calcular_xp_ganado(dificultad: str) -> int:
    """
    Calcula el XP ganado basado en la dificultad de la letra.

    :param dificultad: Dificultad de la letra ('F', 'M', 'D')
    :return: XP ganado
    """
    return XP_POR_DIFICULTAD.get(dificultad, 0)