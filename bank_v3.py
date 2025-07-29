import os
from time import sleep
from abc import ABC, abstractmethod
from datetime import datetime
from random import randint

class Menus:

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

class Conta:
    def __init__(self):
        self._numero = None
        self._cliente = None
        self._agencia = str(randint(1, 1000)).zfill(4)
        self.historico = Historico()
        self.contador_saques = 0
        self._saldo = 0
    
    @property
    def numero(self):
        return self._numero

    @property
    def saldo(self):
        return self._saldo
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    def nova_conta(self, cliente, numero):
        self._cliente = cliente
        self._numero = numero

        return self

    def sacar(self, valor, limite, limite_saques):
        if valor > limite:
            print("Valor solicitado excede o limite de saque.")
            sleep(3)
            return
        elif valor > self.saldo:
            print("Valor solicitado excede o saldo disponível.")
            sleep(3)
            return
        elif valor < 1:
            print("Valor do saque deve ser de, pelo menos, R$1.")
            sleep(3)
            return
        elif self.contador_saques >= limite_saques:
            print("Quantidade de saques excedida.")
            sleep(3)
            return
        
        self._saldo -= valor

        Saque(valor).registrar(self)

        self.contador_saques += 1

        print("Saque realizado com sucesso!")
        sleep(3)


    def depositar(self, valor):
        if valor < 1:
            print("Valor do depósito deve ser de, pelo menos, R$1.")
            return
        
        self._saldo += valor

        Deposito(valor).registrar(self)

        print("Depósito realizado com sucesso!")
        sleep(3)


class ContaCorrente(Conta):
    def __init__(self, limite, limite_saques):
        super().__init__()
        self._limite = limite
        self._limite_saques = limite_saques

    @property
    def limite(self):
        return self._limite
    
    @property
    def limite_saques(self):
        return self._limite_saques


class Cliente:
    def __init__(self, endereco, contas=None):
        self._endereco = endereco
        self._contas = contas if contas else []

    @property
    def contas(self):
        return self._contas
    
    def realizar_transacao(self, conta, valor, transacao, limite=None, limite_saques=None):
        match transacao:
            case "1":
                conta.depositar(valor)
            case "2":
                conta.sacar(valor, limite, limite_saques)

    def adicionar_conta(self, conta):
        self._contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco, contas):
        super().__init__(endereco, contas)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

    @property
    def cpf(self):
        return self._cpf
    
    @property
    def nome(self):
        return self._nome


class Historico:
    def __init__(self, registro=None):
        self._registro = registro if registro else []

    def adicionar_transacao(self, transacao, valor):
        self._registro.append({transacao: valor})

    def __str__(self):
        linhas = []
        #  Adicionar saldo
        for operacao in self._registro:
            for chave, valor in operacao.items():
                hora_local = datetime.now().astimezone()
                hora_formatada = hora_local.strftime("%d/%m/%Y %H:%M:%S")
                linhas.append(f"{chave:10} R${valor:.2f} {hora_formatada.rjust(1)}")
        return "\n".join(linhas) if linhas else "Não há registros em seu extrato."

class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor):
       self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        conta.historico.adicionar_transacao("Depósito:", self.valor)


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        conta.historico.adicionar_transacao("Saque:", self.valor)


class Sessao:
    def __init__(self):
        self._id_contas = 1
        self._usuarios_cadastrados = []

    def sair(self):
        # Método da saída

        os.system("cls" if os.name == "nt" else "clear")
        print("Obrigado por usar o nosso sistema. Ate logo!")
        sleep(3)


    def operacoes(self, pessoa_cadastrada, conta_cadastrada):
        # Método para processar as operações na conta

        while True:
            os.system("cls" if os.name == "nt" else "clear")
            print(f"{conta_cadastrada.cliente.nome.split()[0]} | Agência: {conta_cadastrada.agencia} | Conta: {conta_cadastrada.numero}")
            print(Menus.MENU_PRINCIPAL)

            operacao = input("Escolha a operação: ").strip()
            print()

            match operacao:
                # Depósito

                case "1":
                    try:
                        valor_deposito = float(input("Digite o valor que o(a)" \
                        "senhor(a) deseja depositar: R$").strip())
                    except ValueError:
                        print("Quantia inválida.")
                        sleep(3)
                        continue
                    
                    pessoa_cadastrada.realizar_transacao(conta_cadastrada, valor_deposito, operacao)

                case "2":
                    # Saque

                    try:
                        valor_saque = float(input("Digite o valor que o(a)" \
                        "senhor(a) deseja sacar: R$").strip())
                    except ValueError:
                        print("Quantia inválida.")
                        sleep(3)
                        continue
                    pessoa_cadastrada.realizar_transacao(conta_cadastrada, valor_saque, operacao, conta_cadastrada.limite, conta_cadastrada.limite_saques)

                case "3":
                    # Histórico

                    print(conta_cadastrada.historico)
                    print(f"Saldo:     R${conta_cadastrada.saldo:.2f}")
                    sleep(5)
                case "0":
                    # Sair

                    self.sair()
                    break
                case _:
                    # Opção inválida

                    print("Operação inválida")
                    sleep(3)


    def validador_cpf(self, cpf):
        # Método para validar o CPF

        try:
            if cpf.count(cpf[0]) == len(cpf):
                return False

            soma = 0
            lista_multiplicador_x = zip(list(range(10, 1, -1)), cpf[:9])

            for multiplicador in lista_multiplicador_x:
                soma += multiplicador[0] * int(multiplicador[1])

            resto_divisao =  soma % 11

            digito_verificador_x = 11 - resto_divisao if (11 - resto_divisao) < 10 else 0

            if digito_verificador_x != int(cpf[-2]):
                return False
            
            soma = 0
            lista_multiplicador_y = zip(list(range(11, 1, -1)), cpf[:10])

            for multiplicador in lista_multiplicador_y:
                soma += multiplicador[0] * int(multiplicador[1])

            resto_divisao = soma % 11

            digito_verificador_y = 11 - resto_divisao if (11 - resto_divisao) < 10 else 0

            if digito_verificador_y != int(cpf[-1]):
                return False
            
            return True


        except (ValueError, IndexError):
            return False

    def validador_contas(self, pessoa_cadastrada, agencia, conta):
        # Método para validar a existência da conta

        for conta_cadastrada in pessoa_cadastrada.contas:
            if conta == int(conta_cadastrada.numero) and agencia == conta_cadastrada.agencia:
                return conta_cadastrada
        print("Conta inexistente ou agência incorreta.")
        return None

    def execucao(self):
        # Método para proceder a execução da sessão
        while True:
            os.system("cls" if os.name == "nt" else "clear")
            print(Menus.MENU_CRIACAO)

            escolha_usuario = input("Escolha uma operação: ").strip()

            match escolha_usuario:
                case "1":
                    # Acesso à conta

                    while True:
                        os.system("cls" if os.name == "nt" else "clear")
                        cpf = input("Digite seu CPF (Apenas os números): ").strip()

                        if not self.validador_cpf(cpf):
                            print("CPF inválido!")
                            sleep(3)
                            break

                        pessoa_cadastrada = None

                        for usuario in self._usuarios_cadastrados:
                            if usuario.cpf == cpf:
                                pessoa_cadastrada = usuario
                                break
                        
                        if not pessoa_cadastrada:
                            print("Este usuário não está cadastrado no sistema.")
                            sleep(3)
                            break

                        print(Menus.MENU_CONTAS)

                        escolha_contas = input("Escolha uma opção: ").strip()

                        match escolha_contas:
                            case "1":
                                # Conta existente

                                try:
                                    conta = int(input("Digite a conta que você deseja acessar: ").strip())
                                    agencia = input("Digite a agência da sua conta: ").strip()
                                except ValueError:
                                    print("Agência e/ou conta inválida(s).")
                                    sleep(3)
                                    break
                                
                                conta_cadastrada = self.validador_contas(pessoa_cadastrada, agencia, conta)

                                if conta_cadastrada:
                                    self.operacoes(pessoa_cadastrada, conta_cadastrada)
                                    break
                                else:
                                    sleep(4)
                                    continue
                            case "2":
                                # Adicionar nova conta a usuário já existente
                                # criar lógica para definir limite do número de saques e limite do valor a ser sacado

                                conta_criada = ContaCorrente(500, 3).nova_conta(pessoa_cadastrada, self._id_contas)
                                pessoa_cadastrada.adicionar_conta(conta_criada)
                                
                                self._id_contas += 1

                                print(f"""
                                {pessoa_cadastrada.nome.split()[0]}, sua conta foi criada com sucesso.

                                Dados da conta

                                Agência: {conta_criada.agencia}
                                Conta:   {conta_criada.numero}""")

                                sleep(5)
                case "2":
                    # Criação de Usuários

                    os.system("cls" if os.name == "nt" else "clear")
                    temp_cpf = input("Digite seu CPF (Apenas os números): ").strip()

                    if not self.validador_cpf(temp_cpf):
                            print("CPF inválido!")
                            sleep(3)
                            continue
                    
                    usuario_existente = False

                    for usuario in self._usuarios_cadastrados:
                        if usuario.cpf == temp_cpf:
                            print("Este CPF já existe em nosso sistema.")
                            usuario_existente = True
                            sleep(3)
                            break
                    
                    if usuario_existente:
                        continue
                    
                    while True:
                        temp_nome = input("Digite seu nome: ").strip()

                        if temp_nome:
                            break

                    while True:
                        try:
                            temp_data_nascimento = input("Digite sua data de nascimento (dd/mm/aaaa): ").strip()

                            temp_data_nascimento_formatada = datetime.strptime(temp_data_nascimento, "%d/%m/%Y")

                            break
                        except ValueError:
                            print("Formato Inválido.")


                    print()

                    print("Endereço")
                    temp_rua = input("Rua: ").strip()
                    temp_numero = input("Número: ").strip()
                    temp_bairro = input("Bairro: ").strip()
                    temp_cidade = input("Cidade: ").strip()

                    while True:
                        temp_estado = input("Estado (XX): ").strip()

                        if len(temp_estado) == 2:
                            break
                        else:
                            print()
                            print("Formato inválido.")

                    temp_endereco = f"{temp_rua}, {temp_numero} - {temp_bairro} - {temp_cidade}/{temp_estado}"
                    novo_usuario = PessoaFisica(temp_nome, temp_cpf, temp_data_nascimento_formatada, temp_endereco, [])
                    nova_conta = ContaCorrente(500, 3).nova_conta(novo_usuario, self._id_contas)
                    
                    novo_usuario.adicionar_conta(nova_conta)
                                
                    self._id_contas += 1

                    self._usuarios_cadastrados.append(novo_usuario)

                    os.system("cls" if os.name == "nt" else "clear")

                    print(f"{temp_nome.split()[0]}, é um prazer te receber no Luca's Bank.")

                    sleep(2)

                    print(f"Estes são os dados da sua primeira conta\n\nAgência: {nova_conta.agencia}\nConta:   {nova_conta.numero}")

                    sleep(3)

                    print("Obs.: Anote estas informações, são de suma importância.\n")

                    sleep(5)

                    print(f"Por ora, você recebe R${nova_conta.limite:.2f} de limite de saque, podendo sacar {nova_conta.limite_saques} vezes por dia.\nCom o uso constante e consciente da sua conta, você receberá ótimas oportunidades de crescimento no relacionamento conosco.")
                    
                    sleep(5)

                    os.system("cls" if os.name == "nt" else "clear")

                    print("Agora você será direcionado para a sua conta.")
                    sleep(3)


                    self.operacoes(novo_usuario, nova_conta)

                case "0":
                    # Sair

                    self.sair()
                    break
                case _:
                    # Input inválido

                    print("Opção inválida.")
                    sleep(3)


sessao_atual = Sessao()
sessao_atual.execucao()