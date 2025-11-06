from airwrite.infrastructure.models.silabas import Silaba
from airwrite.infrastructure.models.PerfilUsuario import PerfilUsuario

def esta_bloqueada_silaba(usuario, nombre: str) -> bool:
    # Obtener perfil
    perfil = getattr(usuario, 'perfilusuario', None)
    if not perfil:
        return True

    # Sílabas iniciales desbloqueadas (por ejemplo, BA, BE, CA, CE)
    if nombre in ["BA", "BE", "CA", "CE"]:
        return False

    try:
        silaba_obj = Silaba.objects.get(nombre=nombre)
    except Silaba.DoesNotExist:
        return True

    # Si la sílaba ya fue practicada o está desbloqueada, desbloqueada
    if silaba_obj in perfil.silabas_practicadas.all() or silaba_obj in perfil.silabas_desbloqueadas.all():
        return False

    # Desbloqueo según sílaba anterior (lógica simple: desbloquear si la anterior fue practicada)
    # Para simplificar, desbloquear si el usuario tiene suficiente XP o ha practicado suficientes sílabas anteriores
    # Aquí puedes implementar lógica más compleja basada en el orden alfabético o dificultad

    # Por ejemplo, desbloquear si el usuario tiene al menos 100 XP
    if perfil.xp >= 100:
        return False

    return True
