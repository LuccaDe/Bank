# Luca's Bank 💰 (v2)

Este é um projeto em Python desenvolvido como parte do **Bootcamp Santander | DIO - Backend com Python**.

Nesta segunda versão, o sistema bancário foi expandido para oferecer funcionalidades mais completas, como **cadastro de usuários**, **vinculação de múltiplas contas por CPF**, e **operações bancárias separadas por conta**.

Tudo isso ainda utilizando uma interface simples via terminal.


## 📌 Funcionalidades e regras

- **Cadastro de usuários** com CPF, nome, data de nascimento e endereço completo.
- **Criação de múltiplas contas** bancárias para um mesmo usuário.
- Operações bancárias por conta individual:
  - **Depósito**:
    - Valor mínimo de R$ 1,00
  - **Saque**:
    - Máximo de 3 saques por dia
    - Limite de R$ 500,00 por saque
    - Valor mínimo de R$ 1,00
    - Não é permitido sacar mais do que o saldo disponível
  - **Extrato** com histórico de transações e saldo atualizado.
- **Validação de CPF** e verificação de contas associadas ao usuário.
- Interface limpa com mensagens claras e pausa entre operações para facilitar a leitura.


## 💡 O que foi praticado até aqui

- Modularização com **funções bem definidas** e responsabilidades separadas
- Simulação de **cadastro e autenticação simples**
- Manipulação de **listas de dicionários** para representar usuários e contas
- Validação de entrada e controle de fluxo com `try/except`
- Uso de `os.system()` e `sleep()` para melhorar a experiência no terminal
- Parâmetros posicionais e nomeados em funções (`/` e `*`)
- Regras de negócio mais robustas e realistas


## 🛠️ Tecnologias

- Python 3.13 (sem dependências externas)


## 📈 Próximos passos

- Refatoração para uso de **classes** (Paradigma Orientado a Objetos)
- Implementação de **persistência de dados** (em arquivos `.json` ou `.csv`)
- Criação de uma interface mais amigável via terminal com bibliotecas como `rich` ou `typer`
- Validação real de CPF (com cálculo dos dígitos verificadores)
- Geração automática de extrato em arquivo `.txt` ou `.pdf`


## 📂 Como executar

1. Certifique-se de ter o Python 3 instalado na sua máquina.
2. Clone este repositório:
   ```bash
   git clone https://github.com/LuccaDe/Bank.git
   ```
3. Acesse a pasta do projeto:
   ```bash
   cd Bank
   ```
4. Acesse a branch da versão 2:
   ```bash
   git checkout v2
   ```
4. Execute o script principal:
   ```bash
   python bank_v2.py
   ```


## 🤝 Contribuindo

Sugestões, feedbacks e ideias são muito bem-vindos!  
Sinta-se à vontade para abrir uma issue, comentar ou fazer um fork.

---

**Bootcamp Santander | DIO**  
Projeto: Sistema Bancário com Python  
Desenvolvido por [@LuccaDe](https://github.com/LuccaDe)

