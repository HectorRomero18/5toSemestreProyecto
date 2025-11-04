from airwrite.infrastructure.models.letra import Letra
from airwrite.infrastructure.models.letra_compra import LetraCompra

@staticmethod
def esta_bloqueada(usuario, nombre):
    # Obtener perfil
    perfil = getattr(usuario, 'perfilusuario', None)
    if not perfil:
        return True

    # Letras iniciales desbloqueadas
    if nombre in ["Letra A", "Letra B", "Letra C"]:
        return False

    try:
        letra_obj = Letra.objects.get(nombre=nombre)
    except Letra.DoesNotExist:
        return True

    # Si el usuario ya compró la letra
    if LetraCompra.objects.filter(usuario=usuario, letra=letra_obj).exists():
        return False

    # Desbloqueo según letra anterior
    letra_char = nombre.split()[-1].upper()       
    letra_anterior_char = chr(ord(letra_char) - 1)
    try:
        letra_anterior_obj = Letra.objects.get(nombre=f"Letra {letra_anterior_char}")
    except Letra.DoesNotExist:
        return True

    if letra_anterior_obj in perfil.letras_desbloqueadas.all():
        return False 
    
    # Desbloqueo segun tiene la letra anterior practicada
    if letra_anterior_obj in perfil.letras_practicadas.all():
        return False

    return True
