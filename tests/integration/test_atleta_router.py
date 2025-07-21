import pytest
from httpx import AsyncClient
from workout_api.models.categoria_model import CategoriaModel
from workout_api.models.centro_treinamento_model import CentroTreinamentoModel
from workout_api.models.atleta_model import AtletaModel

class TestAtletaRouter:
    """Testes de integração para rotas de atleta"""
    
    @pytest.fixture
    async def setup_data(self, db_session):
        """Fixture para preparar dados de teste"""
        # Criar categoria
        categoria = CategoriaModel(nome="Scale")
        db_session.add(categoria)
        await db_session.flush()
        
        # Criar centro de treinamento
        centro = CentroTreinamentoModel(
            nome="CT King",
            endereco="Rua X, 123",
            proprietario="Marcos"
        )
        db_session.add(centro)
        await db_session.flush()
        
        await db_session.commit()
        
        return {"categoria_id": categoria.pk_id, "centro_id": centro.pk_id}
    
    @pytest.mark.asyncio
    async def test_create_atleta_success(self, client: AsyncClient, setup_data):
        """Teste: POST /atletas deve criar atleta com sucesso"""
        # Arrange
        atleta_data = {
            "nome": "João Silva",
            "cpf": "12345678901",
            "idade": 25,
            "peso": 75.5,
            "altura": 1.75,
            "sexo": "M",
            "categoria_id": setup_data["categoria_id"],
            "centro_treinamento_id": setup_data["centro_id"]
        }
        
        # Act
        response = await client.post("/atletas/", json=atleta_data)
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["nome"] == "João Silva"
        assert data["cpf"] == "12345678901"
        assert data["idade"] == 25
        assert data["peso"] == 75.5
        assert data["altura"] == 1.75
        assert data["sexo"] == "M"
        assert "pk_id" in data
        assert "created_at" in data
        assert "categoria" in data
        assert "centro_treinamento" in data
    
    @pytest.mark.asyncio
    async def test_create_atleta_duplicate_cpf(self, client: AsyncClient, setup_data):
        """Teste: POST /atletas deve falhar com CPF duplicado"""
        # Arrange - Criar primeiro atleta
        atleta_data = {
            "nome": "João Silva",
            "cpf": "12345678901",
            "idade": 25,
            "peso": 75.5,
            "altura": 1.75,
            "sexo": "M",
            "categoria_id": setup_data["categoria_id"],
            "centro_treinamento_id": setup_data["centro_id"]
        }
        
        await client.post("/atletas/", json=atleta_data)
        
        # Act - Tentar criar segundo atleta com mesmo CPF
        response = await client.post("/atletas/", json=atleta_data)
        
        # Assert
        assert response.status_code == 303
        data = response.json()
        assert "Já existe um atleta cadastrado com o cpf: 12345678901" in data["detail"]
    
    @pytest.mark.asyncio
    async def test_create_atleta_invalid_data(self, client: AsyncClient, setup_data):
        """Teste: POST /atletas deve falhar com dados inválidos"""
        # Arrange
        invalid_data = {
            "nome": "",
            "cpf": "123",  # CPF inválido
            "idade": -5,   # Idade negativa
            "peso": 75.5,
            "altura": 1.75,
            "sexo": "X",   # Sexo inválido
            "categoria_id": setup_data["categoria_id"],
            "centro_treinamento_id": setup_data["centro_id"]
        }
        
        # Act
        response = await client.post("/atletas/", json=invalid_data)
        
        # Assert
        assert response.status_code == 422  # Validation Error
    
    @pytest.mark.asyncio
    async def test_get_atletas_empty(self, client: AsyncClient):
        """Teste: GET /atletas deve retornar lista vazia quando não há atletas"""
        # Act
        response = await client.get("/atletas/")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0
        assert "page" in data
        assert "size" in data
    
    @pytest.mark.asyncio
    async def test_get_atletas_with_data(self, client: AsyncClient, setup_data):
        """Teste: GET /atletas deve retornar lista de atletas"""
        # Arrange - Criar atleta
        atleta_data = {
            "nome": "João Silva",
            "cpf": "12345678901",
            "idade": 25,
            "peso": 75.5,
            "altura": 1.75,
            "sexo": "M",
            "categoria_id": setup_data["categoria_id"],
            "centro_treinamento_id": setup_data["centro_id"]
        }
        
        await client.post("/atletas/", json=atleta_data)
        
        # Act
        response = await client.get("/atletas/")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["total"] == 1
        
        # Verificar que retorna apenas os campos customizados
        atleta = data["items"][0]
        assert "nome" in atleta
        assert "categoria" in atleta
        assert "centro_treinamento" in atleta
        # Não deve conter outros campos
        assert "cpf" not in atleta
        assert "idade" not in atleta
        assert "peso" not in atleta
    
    @pytest.mark.asyncio
    async def test_get_atletas_filter_by_nome(self, client: AsyncClient, setup_data):
        """Teste: GET /atletas?nome=X deve filtrar por nome"""
        # Arrange - Criar dois atletas
        atleta1_data = {
            "nome": "João Silva",
            "cpf": "12345678901",
            "idade": 25,
            "peso": 75.5,
            "altura": 1.75,
            "sexo": "M",
            "categoria_id": setup_data["categoria_id"],
            "centro_treinamento_id": setup_data["centro_id"]
        }
        
        atleta2_data = {
            "nome": "Maria Santos",
            "cpf": "98765432109",
            "idade": 23,
            "peso": 60.0,
            "altura": 1.65,
            "sexo": "F",
            "categoria_id": setup_data["categoria_id"],
            "centro_treinamento_id": setup_data["centro_id"]
        }
        
        await client.post("/atletas/", json=atleta1_data)
        await client.post("/atletas/", json=atleta2_data)
        
        # Act
        response = await client.get("/atletas/?nome=João")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["nome"] == "João Silva"
    
    @pytest.mark.asyncio
    async def test_get_atletas_filter_by_cpf(self, client: AsyncClient, setup_data):
        """Teste: GET /atletas?cpf=X deve filtrar por CPF"""
        # Arrange - Criar atleta
        atleta_data = {
            "nome": "João Silva",
            "cpf": "12345678901",
            "idade": 25,
            "peso": 75.5,
            "altura": 1.75,
            "sexo": "M",
            "categoria_id": setup_data["categoria_id"],
            "centro_treinamento_id": setup_data["centro_id"]
        }
        
        await client.post("/atletas/", json=atleta_data)
        
        # Act
        response = await client.get("/atletas/?cpf=12345678901")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["nome"] == "João Silva"
    
    @pytest.mark.asyncio
    async def test_get_atleta_by_id_success(self, client: AsyncClient, setup_data):
        """Teste: GET /atletas/{id} deve retornar atleta por ID"""
        # Arrange - Criar atleta
        atleta_data = {
            "nome": "João Silva",
            "cpf": "12345678901",
            "idade": 25,
            "peso": 75.5,
            "altura": 1.75,
            "sexo": "M",
            "categoria_id": setup_data["categoria_id"],
            "centro_treinamento_id": setup_data["centro_id"]
        }
        
        create_response = await client.post("/atletas/", json=atleta_data)
        atleta_id = create_response.json()["pk_id"]
        
        # Act
        response = await client.get(f"/atletas/{atleta_id}")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "João Silva"
        assert data["cpf"] == "12345678901"
        assert data["pk_id"] == atleta_id
    
    @pytest.mark.asyncio
    async def test_get_atleta_by_id_not_found(self, client: AsyncClient):
        """Teste: GET /atletas/{id} deve retornar 404 para ID inexistente"""
        # Act
        response = await client.get("/atletas/999")
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "Atleta com id 999 não encontrado" in data["detail"]
    
    @pytest.mark.asyncio
    async def test_update_atleta_success(self, client: AsyncClient, setup_data):
        """Teste: PATCH /atletas/{id} deve atualizar atleta"""
        # Arrange - Criar atleta
        atleta_data = {
            "nome": "João Silva",
            "cpf": "12345678901",
            "idade": 25,
            "peso": 75.5,
            "altura": 1.75,
            "sexo": "M",
            "categoria_id": setup_data["categoria_id"],
            "centro_treinamento_id": setup_data["centro_id"]
        }
        
        create_response = await client.post("/atletas/", json=atleta_data)
        atleta_id = create_response.json()["pk_id"]
        
        update_data = {
            "nome": "João Santos",
            "idade": 26
        }
        
        # Act
        response = await client.patch(f"/atletas/{atleta_id}", json=update_data)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "João Santos"
        assert data["idade"] == 26
        assert data["cpf"] == "12345678901"  # Deve manter campos não alterados
    
    @pytest.mark.asyncio
    async def test_delete_atleta_success(self, client: AsyncClient, setup_data):
        """Teste: DELETE /atletas/{id} deve deletar atleta"""
        # Arrange - Criar atleta
        atleta_data = {
            "nome": "João Silva",
            "cpf": "12345678901",
            "idade": 25,
            "peso": 75.5,
            "altura": 1.75,
            "sexo": "M",
            "categoria_id": setup_data["categoria_id"],
            "centro_treinamento_id": setup_data["centro_id"]
        }
        
        create_response = await client.post("/atletas/", json=atleta_data)
        atleta_id = create_response.json()["pk_id"]
        
        # Act
        response = await client.delete(f"/atletas/{atleta_id}")
        
        # Assert
        assert response.status_code == 204
        
        # Verificar que atleta foi deletado
        get_response = await client.get(f"/atletas/{atleta_id}")
        assert get_response.status_code == 404 