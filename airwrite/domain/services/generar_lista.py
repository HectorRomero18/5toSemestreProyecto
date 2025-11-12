import string

def generar_silabas_ae():
    consonantes = "bcdfghjklmnpqrstvwxyz"
    vocales = "ae"
    silabas = []
    for c in consonantes:
        for v in vocales:
            silabas.append(c + v)
    for v1 in vocales:
        for v2 in vocales:
            silabas.append(v1 + v2)
    return silabas

def generar_lista(tipo: str):
    """
    tipo: 'letras', 'silabas', 'numeros'
    """
    if tipo == "letras":
        return list(string.ascii_uppercase)
    elif tipo == "silabas":
        return [s.upper() for s in generar_silabas_ae()]
    elif tipo == "numeros":
        return [str(i) for i in range(1, 11)]
    else:
        return []
