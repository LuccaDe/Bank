# Luca's Bank 💰

Projeto desenvolvido como parte do **Bootcamp Santander | DIO - Backend com Python**.

Trata-se de uma versão inicial de um sistema bancário simples em terminal, com foco em operações básicas como **depósito**, **saque** e **extrato**.

## 📌 Funcionalidades e regras

- Realizar **depósitos** com valor mínimo de R$ 1,00.
- Realizar **saques**, respeitando:
  - Limite de R$ 500,00 por operação
  - Máximo de 3 saques diários
  - Saldo disponível
  - Valor mínimo de R$ 1,00
- Emitir **extrato** com todas as movimentações e saldo atual.
- Validação de entradas e mensagens claras ao usuário para cada operação.

## 💡 O que foi praticado até aqui

- Estruturas de controle: `if`, `elif`, `while`, `try/except`
- Entrada e saída de dados no terminal
- Listas e tuplas para registro de transações
- Organização de lógica procedural

## 🛠️ Tecnologias

- Python 3.13

## 📈 Próximos passos

- Refatorar o código usando os paradigmas **funcional** e **orientado a objetos**
- Adicionar múltiplos usuários com autenticação simples
- Implementar persistência de dados em arquivos (`.json`, `.csv` ou `.txt`)
- Melhorar a interface no terminal com bibliotecas (como `rich` ou `typer`)

## 📂 Como executar

1. Certifique-se de ter o Python 3 instalado.
2. Clone este repositório:
   ```bash
   git clone https://github.com/LuccaDe/Bank.git
