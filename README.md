# WorkOut API - Academia CrossFit 🏋️‍♂️

API assíncrona para gerenciamento de academia de CrossFit desenvolvida com **FastAPI** seguindo práticas de **TDD (Test Driven Development)**.

## 🚀 Funcionalidades

- ✅ **Gestão de Atletas** com validação de CPF
- ✅ **Categorias de competição** (Scale, RX, etc.)
- ✅ **Centros de treinamento**
- ✅ **Query parameters** para filtros (nome, cpf)
- ✅ **Paginação** com limit/offset
- ✅ **Responses customizados** para endpoints
- ✅ **Tratamento de exceções** de integridade
- ✅ **Testes unitários e de integração** (TDD)
- ✅ **Documentação automática** com OpenAPI

## 🏗️ Arquitetura

A aplicação segue uma **arquitetura em camadas**:

```
workout_api/
├── 📁 configs/          # Configurações (banco, settings)
├── 📁 controllers/      # Lógica de negócio
├── 📁 models/          # Models SQLAlchemy (ORM)
├── 📁 routers/         # Endpoints FastAPI
├── 📁 schemas/         # Schemas Pydantic (validação)
└── 📄 main.py          # Aplicação principal

tests/
├── 📁 unit/            # Testes unitários
├── 📁 integration/     # Testes de integração
├── 📄 conftest.py      # Configurações pytest
└── 📄 factories.py     # Factory Boy (dados de teste)
```

## 🧪 Test Driven Development (TDD)

Este projeto foi desenvolvido seguindo o **ciclo TDD**:

### 🔄 Ciclo Red-Green-Refactor

1. **🔴 Red**: Escrever teste que falha
2. **🟢 Green**: Implementar código mínimo para passar
3. **🔵 Refactor**: Melhorar o código mantendo testes passando

### 📋 Tipos de Teste

- **Testes Unitários**: Testam componentes isolados (schemas, controllers)
- **Testes de Integração**: Testam endpoints completos com banco de dados
- **Fixtures**: Dados de teste reutilizáveis com Factory Boy

### 🎯 Cobertura de Testes

```bash
# Executar todos os testes
make test

# Testes com coverage
make test-cov

# Apenas testes unitários
make test-unit

# Apenas testes de integração
make test-integration
```

## ⚙️ Instalação e Configuração

### 1. 📋 Pré-requisitos

- Python 3.11+
- PostgreSQL 15+
- Docker (opcional)

### 2. 🔧 Setup do Projeto

```bash
# Clonar o repositório
git clone <repo-url>
cd FastApi

# Instalar dependências
make install
# ou pip install -r requirements.txt

# Configurar banco de dados
make db-up
# ou docker-compose up -d

# Executar migrações
make migrate
# ou alembic upgrade head
```

### 3. 🚀 Executar a Aplicação

```bash
# Desenvolvimento
make run
# ou uvicorn workout_api.main:app --reload

# Produção
uvicorn workout_api.main:app --host 0.0.0.0 --port 8000
```

## 📚 Documentação da API

### 🌐 Documentação Interativa

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

### 🛠️ Endpoints Principais

#### 👤 Atletas (`/atletas`)
- `POST /atletas/` - Criar atleta
- `GET /atletas/` - Listar atletas (com filtros e paginação)
- `GET /atletas/{id}` - Buscar atleta por ID
- `PATCH /atletas/{id}` - Atualizar atleta
- `DELETE /atletas/{id}` - Remover atleta

#### 🏷️ Categorias (`/categorias`)
- `POST /categorias/` - Criar categoria
- `GET /categorias/` - Listar categorias
- `GET /categorias/{id}` - Buscar categoria por ID

#### 🏢 Centros de Treinamento (`/centros_treinamento`)
- `POST /centros_treinamento/` - Criar centro
- `GET /centros_treinamento/` - Listar centros
- `GET /centros_treinamento/{id}` - Buscar centro por ID

### 🔍 Query Parameters

```bash
# Filtrar atletas por nome
GET /atletas/?nome=João

# Filtrar atletas por CPF
GET /atletas/?cpf=12345678901

# Paginação
GET /atletas/?page=1&size=10
```

### 📝 Exemplos de Uso

#### Criar Atleta
```bash
curl -X POST "http://localhost:8000/atletas/" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "cpf": "12345678901",
    "idade": 25,
    "peso": 75.5,
    "altura": 1.75,
    "sexo": "M",
    "categoria_id": 1,
    "centro_treinamento_id": 1
  }'
```

## 🛡️ Validações e Tratamento de Erros

### ✅ Validações Implementadas

- **CPF único**: Não permite atletas com CPF duplicado
- **CPF formato**: Apenas números, 11 dígitos
- **Sexo**: Apenas 'M' ou 'F'
- **Valores positivos**: Idade, peso, altura > 0

### ⚠️ Tratamento de Exceções

- **Status 303**: Violação de integridade (CPF/nome duplicado)
- **Status 404**: Recurso não encontrado
- **Status 422**: Dados de entrada inválidos

## 🚧 Desenvolvimento

### 📋 Comandos Úteis

```bash
# Ajuda com todos os comandos
make help

# Limpar arquivos temporários
make clean

# Criar nova migração
make makemigrations msg="Nova funcionalidade"

# Parar banco de dados
make db-down
```

