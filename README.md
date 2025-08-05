# Luca’s Bank 💰 – Versão 4

**Sistema Bancário em Python com CLI Avançada**

Nesta versão 4 do **Luca’s Bank**, ampliamos funcionalidades de persistência, logging e filtragem de extrato, além de introduzir um modo *admin* para iterar sobre todas as contas.

## 🛠 Funcionalidades Principais

1. **Persistência de Dados**

   * Armazenamento de usuários em `users.csv`
   * Armazenamento de contas em `accounts.csv` com histórico serializado em JSON
   * Recuperação automática ao iniciar

2. **Logging de Transações**

   * Decorator `@log_transacao` grava em `log.txt` timestamp, operação, parâmetros e retorno

3. **Cadastro e Autenticação**

   * Validação completa de CPF e formato de data de nascimento
   * Registro de endereço completo

4. **Gerenciamento de Contas**

   * Criação de contas sequenciais com agência aleatória
   * Várias contas por usuário
   * Propriedades de limite e limite de saques configuradas em `ContaCorrente`

5. **Operações Bancárias**

   * Depósito e saque com validações de valor, limite por valor e limites diários
   * Histórico detalhado com data/hora local e opção de filtragem (Depósitos/Saques)

6. **Navegação via Menus CLI**

   * Menus de criação, acesso, operações e extrato (com filtros)
   * Comando secreto `admin` para listar todas as contas via `IteradorContas`


## ⚙️ Estrutura do Código

* **`Menus`**: constantes de texto para todas as telas.
* **`Conta`** e **`ContaCorrente`**: lógica de criação, depósito, saque e logging via decorator.
* **`IteradorContas`**: permite iteração amigável para modo *admin*.
* **`Cliente`** e **`PessoaFisica`**: abstração de usuário e método `realizar_transacao`.
* **`Historico`**: registro de transações com campos `Transação`, `Valor`, `Data/Hora` e método `relatorio` com filtros CLI.
* **`Transacao`** (abstrata) e classes **`Deposito`**, **`Saque`**.
* **`Repositorio`**: persistência em CSV/JSON para usuários e contas.
* **`Sessao`**: fluxo principal de menus, validações, chamadas de operações e persistência ao sair.

## 📝 Changelog (V3 → V4)

* **Persistência** em CSV (`users.csv`, `accounts.csv`)
* **Logging** de métodos críticos em `log.txt`
* **Filtros de extrato** para saques e depósitos
* **IteradorContas** para modo *admin*
* Pequenas melhorias de UX e padronização de pausas
* Correção de Bugs

## 🚧 Próximos Passos

* Criação de **interface gráfica** (Tkinter/Streamlit)
* **Segurança**: criptografia de dados sensíveis (CPF/senha)
* **Testes unitários** e integração contínua (CI)
* **API REST** para acesso remoto
* Adição de banco de dados SQL para persistência de dados

## 📂 Como Executar

1. **Clone e entre na branch v4**:

   ```bash
   git clone https://github.com/LuccaDe/Bank.git
   cd Bank
   git checkout v4
   ```
2. **Certifique-se de usar Python 3.9+**:

   ```bash
   python --version
   ```
3. **Execute o programa**:

   ```bash
   python bank_v4.py
   ```
4. **Saída**: Ao finalizar (`[0] Sair`), os arquivos CSV são atualizados e `log.txt` contém o histórico de chamadas.


## 📈 Exemplo de Uso

```text
$ python bank_v4.py

Bem-Vindo(a) ao Luca's Bank

[1] Já sou cliente
[2] Quero me cadastrar
[0] Sair

Escolha uma opção: 2

Digite seu CPF (Apenas os números): 12345678909
Digite seu nome: Luca Silva
Digite sua data de nascimento (dd/mm/aaaa): 28/07/1995
Rua: Rua A
Número: 123
Bairro: Centro
Cidade: Rio de Janeiro
Estado (XX): RJ

...

[1] Acessar uma conta existente
[2] Criar nova conta

Escolha: 1

...

Luca | Agência: 0420 | Conta: 1

[1] Depositar
[2] Sacar
[3] Extrato
[0] Sair

Escolha a operação: 1

Digite o valor que o(a) senhor(a) deseja depositar: R$200
Depósito realizado com sucesso!

...

-- Extrato (filtrar?) --
[1] Sim
[2] Não
[0] Sair

Escolha: 2
================EXTRATO================
28/07/2025 14:20:00 Depósito:  R$200.00

Saldo:     R$200.00

...

-- Admin Mode --
Digite `admin` no menu inicial para listar todas as contas.
```

## 🤝 Contribuindo

Sugestões, feedbacks e ideias são muito bem-vindos!  
Sinta-se à vontade para abrir uma issue, comentar ou fazer um fork.

---

**Bootcamp Santander | DIO**  
Projeto: Sistema Bancário com Python  
Desenvolvido por [@LuccaDe](https://github.com/LuccaDe)