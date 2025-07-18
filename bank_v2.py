import os
from time import sleep


LIMITE_SAQUE_DIARIO = 3

MENU_CRIACAO = """
Bem-Vindo(a) ao Luca's Bank

[1] Já sou cliente
[2] Quero me cadastrar
[0] Sair
"""
MENU_CONTAS = """
[1] Acessar uma conta existente
[2] Criar uma nova conta
[0] Sair
"""
MENU_PRINCIPAL = """
[1] Depositar
[2] Sacar
[3] Extrato
[0] Sair
"""
numero_conta = 0
contas = []
usuarios = []


def criar_usuario():
    os.system("cls" if os.name == "nt" else "clear")
    cpf = input("Digite seu CPF (Apenas os números): ").strip()

    if not verificador_cpf(cpf):
        print("CPF inválido!")
        sleep(3)
        return

    for cadastro in usuarios:
        if cpf in cadastro["CPF"]:
            print("Este CPF já existe em nosso sistema.")
            sleep(3)
            return
    
    nome = input("Digite seu nome completo: ").strip()
    data_nascimento = input("Digite sua data de nascimento (dd/mm/aaaa): ").strip()

    print()

    print("Endereço")
    rua = input("Rua: ").strip()
    numero = input("Número: ").strip()
    bairro = input("Bairro: ").strip()
    cidade = input("Cidade: ").strip()
    while True:
        estado = input("Estado (XX): ").strip()

        if len(estado) == 2:
            break
        else:
            print()
            print("Formato inválido")

    endereco = f"{rua}, {numero} - {bairro} - {cidade}/{estado}"

    usuarios.append({"CPF": cpf, "NOME": nome, "DATA_DE_NASCIMENTO": data_nascimento, "ENDEREÇO": endereco})
    criar_conta(cpf)

    print(f"""
          O usuário {cpf} foi criado com sucesso.

          Dados da conta

          Agência: 0001
          Conta:   {contas[-1]["NÚMERO_DA_CONTA"]}""")
    sleep(5)


def verificador_cpf(cpf):
    try:
        if len(cpf) != 11:
            return False
        else:
            cpf = int(cpf)
            return True
    except ValueError:
        return False


def criar_conta(cpf):
    global numero_conta

    os.system("cls" if os.name == "nt" else "clear")

    agencia = "0001"
    numero_conta += 1

    contas.append({"USUÁRIO": cpf, "AGÊNCIA": agencia, "NÚMERO_DA_CONTA": numero_conta, "SALDO": .0, "EXTRATO": [], "CONTADOR_SAQUE": 0})



def depositar(saldo_local, extrato):
    os.system("cls" if os.name == "nt" else "clear")

    try:
        deposito = float(input("Digite o valor que o(a) senhor(a) deseja depositar: R$ "))
    except ValueError:
        print("Valor inválido.")
        sleep(3)
        return saldo_local

    print()

    if deposito < 1:
        print("Valor do depósito deve ser de, pelo menos, R$ 1.")
        retorno_menu()
        return saldo_local

    saldo_local += deposito

    extrato.append({"TIPO": "DEPÓSITO", "VALOR": deposito})

    print("Depósito realizado com sucesso!")
    sleep(3)

    return saldo_local


def saque(saldo_local, extrato, contador_saque):
    global LIMITE_SAQUE_DIARIO

    os.system("cls" if os.name == "nt" else "clear")
    try:
        saque = float(input("Digite o valor que o(a) senhor(a) deseja sacar: R$ "))
    except ValueError:
        print("Valor inválido.")
        sleep(3)
        return saldo_local, contador_saque
    
    print()

    if saque > 500:
        print("Valor solicitado excede o limite de saque.")
        retorno_menu()
        return saldo_local, contador_saque
    elif saque > saldo_local:
        print("Valor solicitado excede o saldo disponível.")
        retorno_menu()
        return saldo_local, contador_saque
    elif contador_saque >= LIMITE_SAQUE_DIARIO:
        print("Quantidade de saques excedidas.")
        retorno_menu()
        return saldo_local, contador_saque
    elif saque < 1:
        print("Valor do saque deve ser de, pelo menos, R$ 1.")
        retorno_menu()
        return saldo_local, contador_saque

    contador_saque += 1
    saldo_local -= saque

    extrato.append({"TIPO": "SAQUE", "VALOR": saque})

    print("Saque realizado com sucesso!")
    sleep(3)

    return saldo_local, contador_saque


def exibir_extrato(extrato, /, *, saldo_local):
    os.system("cls" if os.name == "nt" else "clear")

    print("""=======EXTRATO=======
                  
OPERAÇÃO  |  VALOR""")
    print()

    if extrato:
        for i in extrato:
            print(f"{i['TIPO']:10.8s} R$ {i['VALOR']:.2f}")
        print()
        print(f"SALDO:     R$ {saldo_local:.2f}")

        retorno_menu()
    else:
        print("Não há operações registradas no extrato.", end="\n\n")
        retorno_menu()


def operacoes(conta):
    for i in contas:
        if i["NÚMERO_DA_CONTA"] == conta:
            saldo = i["SALDO"]
            extrato = i["EXTRATO"]
            contador_saque = i["CONTADOR_SAQUE"]
            break


    while True:
        os.system("cls" if os.name == "nt" else "clear")

        print(MENU_PRINCIPAL)

        operacao = input("Escolha sua operação: ")
        print()

        if operacao == "1":
            saldo = depositar(saldo, extrato)
        elif operacao == "2":
            saldo, contador_saque = saque(saldo_local=saldo, extrato=extrato, contador_saque=contador_saque)
        elif operacao == "3":
            exibir_extrato(extrato, saldo_local=saldo)
        elif operacao == "0":
            sair()
            break
        else:
            print("Esta não é uma operação válida. Por favor, tente novamente!")
            continue

        for i in contas:
            if i["NÚMERO_DA_CONTA"] == conta:
                i["SALDO"] = saldo
                i["CONTADOR_SAQUE"] = contador_saque
                break

        
def validador_contas(cpf, conta):
    for i in contas:
        if cpf == i["USUÁRIO"] and conta == i["NÚMERO_DA_CONTA"]:
            return True
        
    return False


def sair():
    os.system("cls" if os.name == "nt" else "clear")
    print("Obrigado por usar o nosso sistema. Ate logo!")
    sleep(3)

def retorno_menu():
    input("Pressione ENTER para retornar ao menu...")
    print()

while True:
    os.system("cls" if os.name == "nt" else "clear")
    print(MENU_CRIACAO)

    entrada = input("Escolha uma opção: ")

    if entrada == "1":
        while True:
            os.system("cls" if os.name == "nt" else "clear")
            cpf = input("Digite seu CPF (Apenas os números): ")

            if not verificador_cpf(cpf):
                print("CPF inválido!")
                sleep(3)
                break

            flag = False

            for i in usuarios:
                if cpf == i["CPF"]:
                    flag = True
                    break

            if not flag:
                print("Este usuário não está cadastrado no sistema.")
                sleep(3)
                break

            print(MENU_CONTAS)

            escolha_contas = input("Escolha uma opção: ")

            if escolha_contas == "1":
                conta = int(input("Digite a conta que você deseja acessar: "))

                if validador_contas(cpf, conta):
                    operacoes(conta)
                    break
                else:
                    print("O usuário informado não existe ou não possui a conta descrita.")
                    sleep(5)
                    continue
            elif escolha_contas == "2":
                criar_conta(cpf)
                print(f"""
                Sua conta foi criada com sucesso.

                Dados da conta

                Agência: 0001
                Conta:   {contas[-1]["NÚMERO_DA_CONTA"]}""")

                continue
            elif escolha_contas == "0":
                sair()
            else:
                print("Escolha Inválida")
    elif entrada == "2":
        criar_usuario()
    elif entrada == "0":
        sair()
        break
    else:
        print("Opção inválida.")
        sleep(3)
