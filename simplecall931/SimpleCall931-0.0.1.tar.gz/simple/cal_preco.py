from simple.formata import preco


def aumento(valor, porcentagem, formata=False):
    x = valor + (valor * (porcentagem / 100))
    if formata:
        return preco.real(x)
    else:
        return x


def reducao(valor, porcentagem, formata=False):
    x = valor - (valor * (porcentagem / 100))

    if formata:
        return preco.real(x)
    else:
        return x