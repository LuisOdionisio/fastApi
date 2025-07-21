.PHONY: help
help: ## Mostra esta mensagem de ajuda
	@echo "Comandos disponíveis:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: install
install: ## Instala as dependências
	pip install -r requirements.txt

.PHONY: run
run: ## Executa a aplicação
	uvicorn workout_api.main:app --reload

.PHONY: test
test: ## Executa todos os testes
	pytest

.PHONY: test-unit
test-unit: ## Executa apenas testes unitários
	pytest tests/unit -v

.PHONY: test-integration
test-integration: ## Executa apenas testes de integração
	pytest tests/integration -v

.PHONY: test-cov
test-cov: ## Executa testes com coverage
	pytest --cov=workout_api --cov-report=html --cov-report=term-missing

.PHONY: db-up
db-up: ## Sobe o banco de dados
	docker-compose up -d

.PHONY: db-down
db-down: ## Para o banco de dados
	docker-compose down

.PHONY: migrate
migrate: ## Executa as migrações
	alembic upgrade head

.PHONY: makemigrations
makemigrations: ## Cria uma nova migração
	alembic revision --autogenerate -m "$(msg)"

.PHONY: clean
clean: ## Remove arquivos temporários
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov 