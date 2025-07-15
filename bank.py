LIMITE_SAQUE_DIARIO = 3

menu = """
Bem-Vindo(a) ao Luca's Bank

[1] Depositar
[2] Sacar
[3] Extrato
[0] Sair
"""
saldo = .0
contador_saque = 0
extrato = []

while True:
    print(menu)

    try:
        user_input = int(input("Escolha sua operação: "))
        print()

        if user_input == 1:
            deposito = float(input("Digite o valor que o(a) senhor(a) deseja depositar: R$ "))
            print()

            if deposito < 1:
                print("Valor do depósito deve ser de, pelo menos, R$ 1.")
                input("Pressione ENTER para retornar ao menu...")
                print()
                continue

            saldo += deposito

            extrato.append(("DEPÓSITO", deposito))

            print("Depósito realizado com sucesso!")
        elif user_input == 2:
            saque = float(input("Digite o valor que o(a) senhor(a) deseja sacar: R$ "))
            print()

            if saque > 500:
                print("Valor solicitado excede o limite de saque.")
                input("Pressione ENTER para retornar ao menu...")
                print()
                continue
            elif saque > saldo:
                print("Valor solicitado excede o saldo disponível.")
                input("Pressione ENTER para retornar ao menu...")
                print()
                continue
            elif contador_saque >= LIMITE_SAQUE_DIARIO:
                print("Quantidade de saques excedidas.")
                input("Pressione ENTER para retornar ao menu...")
                print()
                continue
            elif saque < 1:
                print("Valor do saque deve ser de, pelo menos, R$ 1.")
                input("Pressione ENTER para retornar ao menu...")
                print()
                continue

            contador_saque += 1
            saldo -= saque

            extrato.append(("SAQUE", saque))

            print("Saque realizado com sucesso!")
        elif user_input == 3:
            print("""=======EXTRATO=======
                  
OPERAÇÃO  |  VALOR""")
            print()
            for i in extrato:
                print(f"{i[0]:10.8s} R$ {i[1]:.2f}")
            print()
            print(f"SALDO:     R$ {saldo:.2f}")

            input("Pressione ENTER para retornar ao menu...")
            print()
        elif user_input == 0:
            print("Obrigado por usar o nosso sistema. Ate logo!")
            break
        else:
            print("Esta não é uma operação válida. Por favor, tente novamente!")
            continue
    except ValueError:
        print("Digite um valor válido.")