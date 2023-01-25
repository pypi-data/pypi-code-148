from .utils import apresentacao, verificar_com_for, verificar_com_while, fazer_calculo

apresentacao()

# opcao = verificar_com_for(input("Digite sua opção:").lower())
opcao = verificar_com_while(input("Digite sua opção:").lower())

x = input('Coloque o primeiro numero: ')
y = input('Coloque o segundo numero: ')

# calculando
result = fazer_calculo(opcao, x, y)

print(result)