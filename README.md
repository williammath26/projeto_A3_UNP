# TodoList - Aplicação de Gerenciamento de Tarefas

Este é um aplicativo simples de **gerenciamento de tarefas** (To-Do List), onde os usuários podem adicionar, editar, excluir, concluir e visualizar suas tarefas. Ele foi desenvolvido utilizando **Flask**, um framework web em Python, e **MySQL** como banco de dados para armazenar as tarefas e informações dos usuários.

## Tecnologias Usadas

- **Flask**: Framework web para Python usado para criar o backend da aplicação.
- **Flask-Login**: Extensão para gerenciamento de login e autenticação de usuários.
- **SQLAlchemy**: ORM (Object-Relational Mapper) para interagir com o banco de dados MySQL.
- **Werkzeug**: Biblioteca de segurança para hash de senhas.
- **MySQL**: Banco de dados relacional utilizado para armazenar as informações de usuários e tarefas.

## Funcionalidades

- **Login e Logout**: O usuário pode fazer login utilizando o email e senha fixos definidos no código. Após login, pode adicionar, editar, excluir, e concluir tarefas.
- **Gerenciamento de Tarefas**:
  - Adicionar novas tarefas.
  - Editar tarefas existentes.
  - Excluir tarefas.
  - Concluir tarefas (marcar como concluídas).
- **Visualizar Tarefas**: Exibição de tarefas pendentes e concluídas tanto na web quanto via API.

## Banco de Dados

O banco de dados utilizado é **MySQL** e o esquema de tabelas é o seguinte:

- **Tabela `users`**: Armazena as informações de login do usuário (apenas um usuário fixo no código).
- **Tabela `tasks`**: Armazena as tarefas, com campos:
  - `id`: Identificador único da tarefa.
  - `name`: Nome/descrição da tarefa.
  - `completed`: Indica se a tarefa foi concluída (booleano).

### Estrutura do Banco de Dados

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    completed BOOLEAN DEFAULT FALSE
);

## Configuração e Execução

### Requisitos

- **Python 3.x**: O ambiente de desenvolvimento deve ter o Python 3.x instalado.
- **MySQL**: Instale e configure o MySQL, criando o banco de dados chamado `tarefas` e conectando-o ao aplicativo Flask.
- **Bibliotecas**: Instale as dependências do projeto utilizando o `pip`:

```bash
pip install -r requirements.txt
Flask
Flask-Login
Flask-SQLAlchemy
Werkzeug
pymysql
```
## EXECUTE O PROJETO
```bash
python app.py
```

Este projeto fornece uma maneira simples e prática de gerenciar tarefas com funcionalidades como login, adição, edição, exclusão e conclusão de tarefas. Ele utiliza Flask como backend, MySQL como banco de dados e pode ser facilmente testado via Postman para interação com a API
