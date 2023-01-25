from ..soma import somar_numeros

# Apresentacao do programa
def apresentacao():
    print("==== Calculadora do Julio Pereira ====")
    print("Bem vindo a calculadora JPCalc, \
    escolha uma das opções abaixo.")
    print("")
    print("A = Soma")
    print("B = Subtração")
    print("C = Multiplicação")
    print("D = Divisão")

# verificar com for
def verificar_com_for(opcao):
    opcoes = ['a','b','c','d']
    
    for op in opcoes:
        if opcao == op:
            return opcao
            #x += 1
    else:
        opcao = input("Voce precisa colocar uma das opcoes: A, B, C, D: ").lower()
        if not opcao in opcoes: 
            print("infelizmente não consigo fazer o calculo!")
            print("saindo...")
            exit()
        else:
            return opcao


# Verificar com white
def verificar_com_while(opcao):
    opcoes = ['a','b','c','d']
    x = 0
    if opcao in opcoes: x += 1
    # if opcao in opcoes: return opcao

    while x < 1:
        opcao = input("Voce precisa colocar uma das opcoes: A, B, C, D: ").lower()
        if opcao in ['a','b','c','d']: 
            x += 1
            return opcao
    else:
        return opcao
    
def fazer_calculo(operacao, num_1, num_2):
    if operacao == "a":
        # ensinar funcao
        return somar_numeros(num_1,num_2)
    elif operacao == "b":
        return f'{num_1} - {num_1} = {num_1-num_2}'
    elif operacao == "c":
        return f'{num_1} * {num_1} = {num_1*num_2}'
    else:
        return f'{num_1} / {num_2} = {num_1/num_2}'
