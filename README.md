# WorkOut API - Academia CrossFit

API assíncrona para gerenciamento de academia de CrossFit desenvolvida com FastAPI.

## Funcionalidades

- ✅ Gestão de Atletas com validação de CPF
- ✅ Categorias de competição
- ✅ Centros de treinamento
- ✅ Query parameters para filtros (nome, cpf)
- ✅ Paginação com limit/offset
- ✅ Responses customizados
- ✅ Tratamento de exceções de integridade

## Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Configure o banco de dados PostgreSQL

3. Execute as migrações:
```bash
alembic upgrade head
```

4. Inicie o servidor:
```bash
uvicorn workout_api.main:app --reload
```

## Documentação

Acesse a documentação interativa em: http://localhost:8000/docs 