import csv
import json
import os
from time import sleep
from abc import ABC, abstractmethod
from datetime import datetime
from random import randint

PAUSA_LONGA = 5
PAUSA_CURTA = 3

class Menus:
    MENU_CRIACAO = """Bem-Vindo(a) ao Luca's Bank

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

    MENU_FILTRO_1 = """
[1] Sim
[2] Não
[0] Sair
    """

    MENU_FILTRO_2 = """
[1] Depósitos
[2] Saques
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
        self._limite = 0
        self._limite_saques = 0

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

    @property
    def limite(self):
        return self._limite

    @property
    def limite_saques(self):
        return self._limite_saques

    def log_transacao(func):
        def envelope(*args, **kwargs):
            resultado = func(*args, **kwargs)
            try:
                with open("log.txt", "a", encoding="utf-8") as file:
                    file.write("======TIMESTAMP========OPERATION=============================PARAMETERS==================================RETURN===========================\n")
                    file.write(f"{datetime.now().astimezone().strftime("%d/%m/%Y %H:%M:%S")} || {func.__name__.upper():10} || {args} || {resultado}\n")
            except IOError:
                print("Erro ao abrir o arquivo.")
            sleep(PAUSA_CURTA)

            return resultado
        return envelope

    @log_transacao
    def nova_conta(self, cliente, numero):
        self._cliente = cliente
        self._numero = numero

        return self

    @log_transacao
    def sacar(self, valor):
        if valor > self.limite:
            print("Valor solicitado excede o limite de saque.")
            sleep(PAUSA_CURTA)
            return False
        elif valor > self.saldo:
            print("Valor solicitado excede o saldo disponível.")
            sleep(PAUSA_CURTA)
            return False
        elif valor < 1:
            print("Valor do saque deve ser de, pelo menos, R$1.")
            sleep(PAUSA_CURTA)
            return False
        elif self.contador_saques >= self.limite_saques:
            print("Quantidade de saques excedida.")
            sleep(PAUSA_CURTA)
            return False

        self._saldo -= valor

        Saque(valor).registrar(self)

        self.contador_saques += 1

        print("Saque realizado com sucesso!")
        sleep(PAUSA_CURTA)
        return True

    @log_transacao
    def depositar(self, valor):
        if valor < 1:
            print("Valor do depósito deve ser de, pelo menos, R$1.")
            return False

        self._saldo += valor

        Deposito(valor).registrar(self)

        print("Depósito realizado com sucesso!")
        sleep(PAUSA_CURTA)
        return True

    def __repr__(self):
        return f"<Conta: ({self.numero})> <Agência: ({self.agencia})>"


class ContaCorrente(Conta):
    def __init__(self):
        super().__init__()
        self._limite = 500.
        self._limite_saques = 5
    


class IteradorContas:
    def __init__(self, contas):
        self.contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas[self._index]
            return f"""
Titular: {conta.cliente.nome}
Agência: {conta.agencia}
Número:  {conta.numero}
Saldo:   R${conta.saldo:.2f}
"""
        except IndexError:
            raise StopIteration
        finally:
            self._index += 1


class Cliente:
    def __init__(self, endereco, contas=None):
        self._endereco = endereco
        self._contas = contas if contas else []

    @property
    def contas(self):
        return self._contas
    
    @property
    def endereco(self):
        return self._endereco

    def realizar_transacao(self, conta, valor, transacao):
        match transacao:
            case "1":
                conta.depositar(valor)
            case "2":
                conta.sacar(valor)

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
    
    @property
    def data_nascimento(self):
        return self._data_nascimento

    def __repr__(self):
        return f"<Cliente: ({self.cpf})>"



class Historico:
    def __init__(self, registro=None):
        self._registro = registro if registro else []

    @property
    def registro(self):
        return self._registro

    def adicionar_transacao(self, transacao, valor):
        hora_local = datetime.now().astimezone()
        self._registro.append({"Transação": transacao, "Valor": valor, "Data/Hora": hora_local})

    def relatorio(self, transacao=None):
        os.system("cls" if os.name == "nt" else "clear")
        linhas = []
        print("================EXTRATO================")

        for operacao in self._registro:
            if transacao is None or transacao.lower() == operacao["Transação"].lower():
                hora_formatada = operacao["Data/Hora"].strftime("%d/%m/%Y %H:%M:%S")
                linhas.append(f"{hora_formatada.rjust(1)} {operacao['Transação']:10} R${operacao['Valor']:.2f}")

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

class Repositorio:
    def __init__(self):
        self.usuarios_cadastrados = []
        self.contas_cadastradas = []
        self.id_contas = 1

    def cadastrar_dados(self, usuarios_cadastrados, contas_cadastradas):
        # Adicionar verificação de duplicidade     
        try:
            with open("users.csv", "w", newline="", encoding="utf-8") as file:
                campos = ["nome", "cpf", "data_nascimento", "endereco", "contas"]
                writer = csv.DictWriter(file, fieldnames=campos)
                
                writer.writeheader()

                for usuario in usuarios_cadastrados:
                    dados_usuario = {
                        "nome": usuario.nome,
                        "cpf": usuario.cpf,
                        "data_nascimento": usuario.data_nascimento.strftime("%d/%m/%Y"),
                        "endereco": usuario.endereco,
                        "contas": [f"Conta: {c.numero} | Agência: {c.agencia} | Saldo: {c.saldo}" for c in usuario.contas]
                    }
                    writer.writerow(dados_usuario)

            with open("accounts.csv", "w", newline="", encoding="utf-8") as file:
                campos = ["cliente", "numero", "agencia", "saldo", "limite", "limite_saques", "historico"]
                writer = csv.DictWriter(file, fieldnames=campos)
                
                writer.writeheader()

                for conta in contas_cadastradas:
                    dados_conta = {
                        "cliente": conta.cliente.cpf,
                        "numero": conta.numero,
                        "agencia": conta.agencia,
                        "saldo": conta.saldo,
                        "limite": conta.limite,
                        "limite_saques": conta.limite_saques,
                        "historico": json.dumps([{
                            "Transação": item["Transação"],
                            "Valor": item["Valor"],
                            "Data/Hora": item["Data/Hora"].isoformat()} for item in conta.historico.registro])
                    }

                    writer.writerow(dados_conta)
        except Exception as e:
            print(f"Ocorreu um erro ao carregar os dados: {e}.")

    def recuperar_dados(self):
        try:
            with open("users.csv", "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
            
                for usuario in reader:                    
                    self.usuarios_cadastrados.append(PessoaFisica(
                        usuario["nome"],
                        usuario["cpf"],
                        datetime.strptime(usuario["data_nascimento"], "%d/%m/%Y"),
                        usuario["endereco"],
                        []
                    ))
            
            with open("accounts.csv", "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for conta in reader:
                    for usuario in self.usuarios_cadastrados:
                        if conta["cliente"] == usuario.cpf:
                            nova_conta = ContaCorrente()

                            nova_conta._cliente = usuario
                            nova_conta._numero = int(conta["numero"])
                            nova_conta._agencia = conta["agencia"]
                            nova_conta._saldo = float(conta["saldo"])
                            nova_conta._limite = float(conta["limite"])
                            nova_conta._limite_saques = int(conta["limite_saques"])

                            lista_historico = json.loads(conta["historico"])

                            for transacao in lista_historico:
                                transacao["Data/Hora"] = datetime.fromisoformat(transacao["Data/Hora"])

                            nova_conta.historico._registro = lista_historico

                            self.contas_cadastradas.append(nova_conta)

                            usuario.adicionar_conta(nova_conta)
                            self.id_contas += 1
                            break
        except FileNotFoundError:
            print("Iniciando um novo repositório.")
            sleep(PAUSA_CURTA)
        except Exception as e:
            print(f"Ocorreu um erro ao carregar os dados: {e}.")
            sleep(PAUSA_LONGA)

        return self.usuarios_cadastrados, self.contas_cadastradas, self.id_contas                 


class Sessao:
    def __init__(self):
        self._repositorio = Repositorio()
        self._usuarios_cadastrados, self._contas_cadastradas, self._id_contas = self._repositorio.recuperar_dados()

    def sair(self):
        # Método da saída

        os.system("cls" if os.name == "nt" else "clear")
        print("Obrigado por usar o nosso sistema. Ate logo!")
        sleep(PAUSA_CURTA)

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
                        valor_deposito = float(input("Digite o valor que o(a) senhor(a) deseja depositar: R$").strip())
                    except ValueError:
                        print("Quantia inválida.")
                        sleep(PAUSA_CURTA)
                        continue

                    pessoa_cadastrada.realizar_transacao(conta_cadastrada, valor_deposito, operacao)

                case "2":
                    # Saque

                    try:
                        valor_saque = float(input("Digite o valor que o(a)"
                                            "senhor(a) deseja sacar: R$").strip())
                    except ValueError:
                        print("Quantia inválida.")
                        sleep(PAUSA_CURTA)
                        continue
                    pessoa_cadastrada.realizar_transacao(conta_cadastrada, valor_saque, operacao)

                case "3":
                    # Histórico

                    os.system("cls" if os.name == "nt" else "clear")
                    print(Menus.MENU_FILTRO_1)
                    escolha_filtro = input("Deseja filtrar seu extrato? ").strip()

                    match escolha_filtro:
                        case "1":
                            os.system("cls" if os.name == "nt" else "clear")
                            print(Menus.MENU_FILTRO_2)
                            filtro = input("Escolha o filtro desejado: ").strip()

                            match filtro:
                                case "1":
                                    print(conta_cadastrada.historico.relatorio("Depósito:"), end="\n\n")
                                    print(f"Saldo:     R${conta_cadastrada.saldo:.2f}")
                                    sleep(PAUSA_LONGA)
                                case "2":
                                    print(conta_cadastrada.historico.relatorio("Saque:"), end="\n\n")
                                    print(f"Saldo:     R${conta_cadastrada.saldo:.2f}")
                                    sleep(PAUSA_LONGA)
                                case "0":
                                    # Sair

                                    self.sair()
                                    break
                                case _:
                                    # Opção inválida

                                    print("Operação inválida")
                                    sleep(PAUSA_CURTA)
                        case "2":
                            print(conta_cadastrada.historico.relatorio(), end="\n\n")
                            print(f"Saldo:     R${conta_cadastrada.saldo:.2f}")
                            sleep(PAUSA_LONGA)
                        case "0":
                            # Sair

                            self.sair()
                            break
                        case _:
                            # Opção inválida

                            print("Operação inválida")
                            sleep(PAUSA_CURTA)
                case "0":
                    # Sair

                    self.sair()
                    break
                case _:
                    # Opção inválida

                    print("Operação inválida")
                    sleep(PAUSA_CURTA)

    def validador_cpf(self, cpf):
        # Método para validar o CPF

        try:
            if cpf.count(cpf[0]) == len(cpf):
                return False

            soma = 0
            lista_multiplicador_x = zip(list(range(10, 1, -1)), cpf[:9])

            for multiplicador in lista_multiplicador_x:
                soma += multiplicador[0] * int(multiplicador[1])

            resto_divisao = soma % 11

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
                            sleep(PAUSA_CURTA)
                            break

                        pessoa_cadastrada = None

                        for usuario in self._usuarios_cadastrados:
                            if usuario.cpf == cpf:
                                pessoa_cadastrada = usuario
                                break

                        if not pessoa_cadastrada:
                            print("Este usuário não está cadastrado no sistema.")
                            sleep(PAUSA_CURTA)
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
                                    sleep(PAUSA_CURTA)
                                    break

                                conta_cadastrada = self.validador_contas(pessoa_cadastrada, agencia, conta)

                                if conta_cadastrada:
                                    self.operacoes(pessoa_cadastrada, conta_cadastrada)
                                    break
                                else:
                                    sleep(PAUSA_LONGA)
                                    continue
                            case "2":
                                # Adicionar nova conta a usuário já existente
                                # lógica para definir limite do número de saques e limite do valor a ser sacado

                                os.system("cls" if os.name == "nt" else "clear")

                                conta_criada = ContaCorrente().nova_conta(
                                    pessoa_cadastrada,
                                    self._id_contas
                                    )
                                pessoa_cadastrada.adicionar_conta(conta_criada)

                                self._contas_cadastradas.append(conta_criada)

                                self._id_contas += 1

                                print(f"""
{pessoa_cadastrada.nome.split()[0]}, sua conta foi criada com sucesso.

Dados da conta

Agência: {conta_criada.agencia}
Conta:   {conta_criada.numero}""")

                                sleep(PAUSA_LONGA)

                                os.system("cls" if os.name == "nt" else "clear")

                                print("Agora você será direcionado para a sua conta.")
                                sleep(PAUSA_CURTA)

                                self.operacoes(pessoa_cadastrada, conta_criada)
                                break
                            case "0":
                                # Sair

                                self.sair()
                                break
                            case _:
                                 # Input inválido

                                print("Opção inválida.")
                                sleep(PAUSA_CURTA)
                case "2":
                    # Criação de Usuários

                    os.system("cls" if os.name == "nt" else "clear")
                    temp_cpf = input("Digite seu CPF (Apenas os números): ").strip()

                    if not self.validador_cpf(temp_cpf):
                        print("CPF inválido!")
                        sleep(PAUSA_CURTA)
                        continue

                    usuario_existente = False

                    for usuario in self._usuarios_cadastrados:
                        if usuario.cpf == temp_cpf:
                            print("Este CPF já existe em nosso sistema.")
                            usuario_existente = True
                            sleep(PAUSA_CURTA)
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
                        temp_estado = input("Estado (XX): ").strip().upper()

                        if len(temp_estado) == 2:
                            break
                        else:
                            print()
                            print("Formato inválido.")

                    temp_endereco = f"{temp_rua}, {temp_numero} - {temp_bairro} - {temp_cidade}/{temp_estado}"
                    novo_usuario = PessoaFisica(temp_nome, temp_cpf, temp_data_nascimento_formatada, temp_endereco, [])
                    nova_conta = ContaCorrente().nova_conta(novo_usuario, self._id_contas)

                    novo_usuario.adicionar_conta(nova_conta)

                    self._id_contas += 1

                    self._usuarios_cadastrados.append(novo_usuario)
                    self._contas_cadastradas.append(nova_conta)

                    os.system("cls" if os.name == "nt" else "clear")

                    print(f"{temp_nome.split()[0]}, é um prazer te receber no Luca's Bank.")

                    sleep(PAUSA_CURTA)

                    print(f"Estes são os dados da sua primeira conta\n\nAgência: {nova_conta.agencia}\nConta:   {nova_conta.numero}")

                    sleep(PAUSA_CURTA)

                    print("Obs.: Anote estas informações, são de suma importância.\n")

                    sleep(PAUSA_LONGA)

                    print(f"Por ora, você recebe R${nova_conta.limite:.2f} de limite de saque, podendo sacar {nova_conta.limite_saques} vezes por dia.\nCom o uso constante e consciente da sua conta, você receberá ótimas oportunidades de crescimento no relacionamento conosco.")

                    sleep(PAUSA_LONGA)

                    os.system("cls" if os.name == "nt" else "clear")

                    print("Agora você será direcionado para a sua conta.")
                    sleep(PAUSA_CURTA)

                    self.operacoes(novo_usuario, nova_conta)
                case "admin":
                    os.system("cls" if os.name == "nt" else "clear")

                    if self._usuarios_cadastrados:
                        for conta in IteradorContas(self._contas_cadastradas):
                            print(conta)
                    else:
                        print("Nenhum usuário cadastrado.")

                    sleep(PAUSA_LONGA)
                case "0":
                    # Sair

                    self.sair()
                    self._repositorio.cadastrar_dados(self._usuarios_cadastrados, self._contas_cadastradas)
                    break
                case _:
                    # Input inválido

                    print("Opção inválida.")
                    sleep(PAUSA_CURTA)

sessao_atual = Sessao()
sessao_atual.execucao()
