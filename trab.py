import sys

#Funcao para ler os numeros do arquivo
def abrir_arquivo(nome_arquivo):
    file = open(nome_arquivo, "r")
    lista = file.readlines()
    file.close()
    return lista

#Funcao para transformar a base binara em decimal
def binario_para_decimal(numero):
    decimal = 0
    p = 0
    for digito in reversed(numero):
        if int(digito) == 0:
            decimal += 0
        elif int(digito) == 1:
            decimal+= 2**p
        p+= 1
    return decimal

#Funcao para transformar a base binaria em sinal e magnitude em base decimal
def sm_para_decimal(numero):
    decimal = binario_para_decimal(numero[1:32])
    if(numero[0] == '1'):
        decimal *= -1
    return decimal

#Funcao para descobrir qual a maior magnitude entre dois numeros em SM
def maior_magnitude_sm(numero1,numero2):
    atual=1
    while(numero1[atual] == numero2[atual]):
        atual +=1
    if numero1[atual-1] == "1":
        return True
    else:
        return False

#Funcao para somar os numeros na base binaria com sinal de magnitude
def adicao_sm(numero1,numero2):
    if(numero1[0] == numero2[0]):
        soma = adicao_bin(numero1,numero2)
        soma += numero1[0]
    else:
        if maior_magnitude_sm(numero1, numero2):
            soma = subtracao_sm(numero1, numero2)
            soma += numero1[0]
        else:
            soma = subtracao_sm(numero2, numero1)
            soma += numero2[0]
    return soma[::-1]

#Funcao para somar os numeros na base binaria
def adicao_bin(numero1, numero2): 
    soma  = ""
    temp = 0
    for i in range((len(numero1)-1),0,-1):
        if numero1[i] == numero2[i]:
            if temp == 1:
                soma += "1"
                temp = 0
            else:
                soma += "0"
            if numero1[i] == "1":
                temp = 1
        else:
            if temp == 1:
                soma += "0"
                temp = 1
            else:
                soma += "1"
    return soma

#Funcao para subtrair os numeros na base binaria com sinal de magnitude
def subtracao_sm(numero1, numero2): 
    soma  = ""
    temp = '0'
    emprestado = 0
    for i in range((len(numero1)-1)-1,0,-1):
        if emprestado == 1:
            temp = '0'
            if numero1[i] == '1':
                emprestado = 0
        else:
            temp = numero1[i]
        if temp == numero2[i]:
            soma += '0'
        else:
            soma += '1'
            if temp == '0':
                emprestado = 1
    return soma

#Funcao para inverter o sinal de um numero em SM
def inverte_sinal_sm(numero):
    if numero[0] == '1':
        return '0' + numero[1:32]
    else:
        return '1' + numero[1:32]

#Funcao para transformar a base binaria em complemento de dois em base decimal
def c2_para_decimal(numero):
    if(numero[0] == '0'):
        return binario_para_decimal(numero[1:32])
        
    else:
        return binario_para_decimal(inverte_sinal_c2(numero)) * -1    

#Funcao para inverter o sinal de um numero em C2
def inverte_sinal_c2(numero):
    c2 = ""
    for digito in numero:
        if digito == "0":
            c2 += "1"
        elif digito == "1":
            c2 += "0"
    c2 = adicao_c2(c2, "00000000000000000000000000000001")
    return c2

def adicao_c2(numero1, numero2):
    soma = adicao_bin('0' + numero1, '0' + numero2)
    return soma[::-1]

try:
    lista = abrir_arquivo(sys.argv[1])
except:
    print("Erro ao abrir o arquivo")
    sys.exit()

atual = 0
while atual+1 <= len(lista):
    numero1, numero2 = lista[atual].strip('\n'), lista[atual+1].strip('\n')
    # Sinal e Magnitude
    ## Decimal
    print(f'{sm_para_decimal(numero1):_.0f}'.replace("_","."))
    print(f'{sm_para_decimal(numero2):_.0f}'.replace("_","."))
    print()
    ## Soma
    soma = adicao_sm(numero1, numero2)
    print(soma)
    ## Subtracao
    subtracao = adicao_sm(numero1, inverte_sinal_sm(numero2))
    print(subtracao)
    print()
    ## Soma em decimal
    print(f'{sm_para_decimal(soma):_.0f}'.replace("_","."))
    ## Subtracao em decimal
    print(f'{sm_para_decimal(subtracao):_.0f}'.replace("_","."))
    print()
    # Complemento de 2
    ## Decimal
    print(f'{c2_para_decimal(numero1):_.0f}'.replace("_","."))
    print(f'{c2_para_decimal(numero2):_.0f}'.replace("_","."))
    print()
    ## Soma
    soma = adicao_c2(numero1, numero2)
    print(soma)
    ## Subtracao
    subtracao = adicao_c2(numero1, inverte_sinal_c2(numero2))
    print(subtracao)
    print()
    ## Soma em decimal
    print(f'{c2_para_decimal(soma):_.0f}'.replace("_","."))
    ## Subtracao em decimal
    print(f'{c2_para_decimal(subtracao):_.0f}'.replace("_","."))
    print()
    atual += 3