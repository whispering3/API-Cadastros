# API de Gestão de Clientes e Pedidos

Sistema de backend desenvolvido para gerenciar o ciclo de vida do usuário (CRUD) e a vinculação de pedidos.

## Demo

- 🚀 **Dashboard (Front-end):** [api-gcc-production.up.railway.app/](https://api-gcc-production.up.railway.app/)
- 📄 **Documentação (Swagger):** [api-gcc-production.up.railway.app/docs](https://api-gcc-production.up.railway.app/docs)
## Stack

| Categoria | Tecnologia |
| :--- | :--- |
| **Linguagem** | Python 3.11+ |
| **Framework** | FastAPI (Swagger/OpenAPI nativo) |
| **Banco de Dados** | PostgreSQL |
| **ORM** | SQLAlchemy 2.0 |
| **Autenticação** | JWT |
| **Hashing** | Argon2 |
| **Containerização** | Docker e Docker Compose |

## Endpoints

| Funcionalidade | Método | Endpoint | Descrição |
| :--- | :---: | :--- | :--- |
| Cadastro | `POST` | `/api/v1/users/register` | Criação de usuário com CPF, RG, Nome, Idade, etc. |
| Login | `POST` | `/api/v1/auth/login` | Autenticação via Login/E-mail e Senha para gerar token |
| Listar Todos | `GET` | `/api/v1/users` | Exibição de todos os usuários cadastrados |
| Atualizar | `PATCH` | `/api/v1/users/{id}` | Alteração parcial ou total de dados |
| Deletar | `DELETE` | `/api/v1/users/{id}` | Exclusão física ou lógica (soft delete via `?physical=true`) |
| Criar Pedido | `POST` | `/api/v1/orders` | Vincula descrição ao ID do usuário autenticado |
| Listar Pedidos | `GET` | `/api/v1/orders` | Filtros por usuário ou listagem geral |

## Como Rodar

### Pré-requisitos

- Docker e Docker Compose instalados.

### 1. Clone o repositório

```bash
git clone https://github.com/whispering3/API-Cadastros.git
cd api-cadastro-gcc
```

### 2. Configure as variáveis de ambiente

Copie o arquivo de exemplo e edite conforme necessário:

```bash
cp .env.example .env
```

| Variável | Descrição | Exemplo |
| :--- | :--- | :--- |
| `DATABASE_URL` | String de conexão com o banco | `postgresql://user:pass@db:5432/dbname` |
| `SECRET_KEY` | Chave para criptografia e assinatura JWT | `sua-chave-secreta` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Tempo de expiração da sessão | `30` |

### 3. Suba os containers

```bash
docker-compose up --build
```

A API estará disponível em `http://localhost:8000`.

## Arquitetura do Projeto

O projeto segue os princípios de **Clean Architecture**, com separação clara de responsabilidades:

```
app/
├── models/     # Definições das tabelas do banco de dados
├── schemas/    # Validadores de entrada e saída (Pydantic)
├── services/   # Lógica de negócio (Business Logic)
└── routers/    # Definição das rotas e injeção de dependências
```

### Decisões de Design

- **Hashing seguro:** Argon2 garante que senhas nunca sejam armazenadas em texto plano.
- **Validação:** CPF e e-mail são validados via Pydantic (lógica matemática + formato).
- **Relacionamento:** A tabela `orders` possui Foreign Key apontando para o ID do usuário.
- **Soft Delete:** Registros deletados são marcados como inativos (`is_active = false`, `deleted_at = timestamp`) em vez de removidos fisicamente. A exclusão física é opcional via `?physical=true`.

---

Desenvolvido por **Danilo Souza**
