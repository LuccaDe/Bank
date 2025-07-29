# Luca’s Bank 💰 – Versão 3

Este é um projeto em Python desenvolvido como parte do **Bootcamp Santander | DIO - Backend com Python**.

Este repositório contém a **terceira versão** do *Luca’s Bank*, um sistema bancário de linha de comando desenvolvido em Python, focado em boas práticas de Programação Orientada a Objetos (POO) e experiência do usuário.

## 🛠 Funcionalidades

* **Cadastro de Usuário (Pessoa Física)**

  * Validação de CPF com dígitos verificadores
  * Entrada de data de nascimento formatada
  * Endereço completo (rua, número, bairro, cidade/estado)
* **Gerenciamento de Contas**

  * Várias contas por usuário
  * Geração automática de agência (código aleatório) e número sequencial de conta
* **Operações Bancárias**

  * Depósito: mínimo R\$ 1, registro em histórico
  * Saque: mínimo R\$ 1, limite por valor e quantidade diária, registro em histórico
* **Histórico de Transações**

  * Exibição de tipo (Depósito/Saque), valor e timestamp local (fuso horário do usuário)
  * Saldo disponível exibido junto
* **Navegação via Menus CLI**

  * Menus de criação, acesso a contas e operações internas
  * Uso de `match/case` para fluxo de seleção

## ⚙️ Estrutura do Código

* **`Menus`**: Strings constantes para exibição de menus.
* **`Conta` / `ContaCorrente`**: Lógica de saldo, limites e contador de saques.
* **`Cliente` / `PessoaFisica`**: Armazenamento de contas e método `realizar_transacao`.
* **`Historico`**: Registro e impressão de transações com data/hora local.
* **`Transacao`** (abstrata) e classes **`Deposito`**, **`Saque`**.
* **`Sessao`**: Controla o fluxo principal, validação de CPF, criação e acesso de contas.

## 🗒️ Changelog (V2 → V3)

* Adicionado timestamp local em cada transação
* Centralização da lógica de transação em `Cliente.realizar_transacao`
* Validação de data de nascimento com `datetime.strptime`
* Aprimoramentos gerais de UX (mensagens e espaçamentos)

## 📈 Próximos Passos

* Persistência em JSON/CSV para manter dados entre sessões
* Autenticação com senha/encriptação básica
* Interface aprimorada com `Typer` ou `Rich`
* Testes automatizados com `pytest`

## 📂 Como Executar

1. **Clone o repositório e acesse a branch v3**:

   ```bash
   git clone https://github.com/LuccaDe/Bank.git
   cd Bank
   git checkout v3
   ```
2. **Verifique sua versão do Python** (recomendado 3.9+):

   ```bash
   python --version
   ```
3. **Execute o script principal**:

   ```bash
   python bank_v3.py
   ```
4. **Siga as instruções na tela** para cadastrar usuário, criar/selecionar conta e realizar operações.

## 📈 Exemplos de Uso

```text
$ python bank_v3.py

Bem-Vindo(a) ao Luca's Bank

[1] Já sou cliente
[2] Quero me cadastrar
[0] Sair

Escolha uma operação: 2

Digite seu CPF (Apenas os números): 12345678909
Digite seu nome: Luca Silva
Digite sua data de nascimento (dd/mm/aaaa): 28/07/1995

...

[1] Acessar uma conta existente
[2] Criar uma nova conta
[0] Sair

Escolha uma opção: 1

...

Luca | Agência: 0420 | Conta: 1

[1] Depositar
[2] Sacar
[3] Extrato
[0] Sair

Escolha a operação: 1

Digite o valor que o(a) senhor(a) deseja depositar: R$100
Depósito realizado com sucesso!
```

## 🤝 Contribuindo

Sugestões, feedbacks e ideias são muito bem-vindos!  
Sinta-se à vontade para abrir uma issue, comentar ou fazer um fork.

---

**Bootcamp Santander | DIO**  
Projeto: Sistema Bancário com Python  
Desenvolvido por [@LuccaDe](https://github.com/LuccaDe)