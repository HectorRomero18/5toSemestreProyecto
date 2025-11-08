from airwrite.infrastructure.models.silabas import Silaba
from airwrite.infrastructure.models.PerfilUsuario import PerfilUsuario
def esta_bloqueada_silaba(usuario, nombre: str) -> bool:
    perfil = getattr(usuario, 'perfilusuario', None)
    if not perfil:
        return True
    
    if nombre in ["Silaba ba", "Silaba be", "Silaba ca"]:
        return False

    try:
        silaba_obj = Silaba.objects.get(nombre=nombre)
    except Silaba.DoesNotExist:
        return True

    if silaba_obj in perfil.silabas_practicadas.all() or silaba_obj in perfil.silabas_desbloqueadas.all():
        return False

    # Obtener las letras que forman la sílaba
    silaba_texto = nombre.replace("Silaba", "").strip()

    letras_silabas = [f"Letra {l.upper()}" for l in silaba_texto if l.isalpha()]
    # print("Letras de la sílaba:", letras_silabas)

    # Letras desbloqueadas del perfil
    letras_desbloqueadas = set(
        l.lower() for l in perfil.letras_desbloqueadas.values_list('nombre', flat=True)
    )
    # print("Letras desbloqueadas:", letras_desbloqueadas)

    # Si todas las letras están desbloqueadas → sílaba desbloqueada
    bloqueado = all(letra.lower() in letras_desbloqueadas for letra in letras_silabas)
    if bloqueado:
        perfil.silabas_desbloqueadas.add(silaba_obj)
        perfil.save()
        return False
    
    

    return True
