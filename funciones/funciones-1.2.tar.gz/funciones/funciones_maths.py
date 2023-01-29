def es_par(valor):
    if valor % 2 == 0:
        return True
    else:
        return False

def es_impar(valor):
    if es_par(valor):
        return False
    else:
        return True
