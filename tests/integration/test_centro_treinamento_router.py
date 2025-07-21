import pytest
from httpx import AsyncClient

class TestCentroTreinamentoRouter:
    """Testes de integração para rotas de centro de treinamento"""
    
    @pytest.mark.asyncio
    async def test_create_centro_success(self, client: AsyncClient):
        """Teste: POST /centros_treinamento deve criar centro com sucesso"""
        # Arrange
        centro_data = {
            "nome": "CT King",
            "endereco": "Rua X, 123",
            "proprietario": "Marcos"
        }
        
        # Act
        response = await client.post("/centros_treinamento/", json=centro_data)
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["nome"] == "CT King"
        assert data["endereco"] == "Rua X, 123"
        assert data["proprietario"] == "Marcos"
        assert "pk_id" in data
    
    @pytest.mark.asyncio
    async def test_create_centro_duplicate_name(self, client: AsyncClient):
        """Teste: POST /centros_treinamento deve falhar com nome duplicado"""
        # Arrange - Criar primeiro centro
        centro_data = {
            "nome": "CT King",
            "endereco": "Rua X, 123",
            "proprietario": "Marcos"
        }
        await client.post("/centros_treinamento/", json=centro_data)
        
        # Act - Tentar criar segundo centro com mesmo nome
        response = await client.post("/centros_treinamento/", json=centro_data)
        
        # Assert
        assert response.status_code == 303
        data = response.json()
        assert "Já existe um centro de treinamento cadastrado com o nome: CT King" in data["detail"]
    
    @pytest.mark.asyncio
    async def test_create_centro_invalid_data(self, client: AsyncClient):
        """Teste: POST /centros_treinamento deve falhar com dados inválidos"""
        # Arrange
        invalid_data = {
            "nome": "",
            "endereco": "",
            "proprietario": ""
        }
        
        # Act
        response = await client.post("/centros_treinamento/", json=invalid_data)
        
        # Assert
        assert response.status_code == 422
    
    @pytest.mark.asyncio
    async def test_get_centros_empty(self, client: AsyncClient):
        """Teste: GET /centros_treinamento deve retornar lista vazia quando não há centros"""
        # Act
        response = await client.get("/centros_treinamento/")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data == []
    
    @pytest.mark.asyncio
    async def test_get_centros_with_data(self, client: AsyncClient):
        """Teste: GET /centros_treinamento deve retornar lista de centros"""
        # Arrange - Criar centros
        centro1_data = {
            "nome": "CT King",
            "endereco": "Rua X, 123",
            "proprietario": "Marcos"
        }
        centro2_data = {
            "nome": "CT Queen",
            "endereco": "Rua Y, 456",
            "proprietario": "Ana"
        }
        
        await client.post("/centros_treinamento/", json=centro1_data)
        await client.post("/centros_treinamento/", json=centro2_data)
        
        # Act
        response = await client.get("/centros_treinamento/")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        nomes = [centro["nome"] for centro in data]
        assert "CT King" in nomes
        assert "CT Queen" in nomes
    
    @pytest.mark.asyncio
    async def test_get_centro_by_id_success(self, client: AsyncClient):
        """Teste: GET /centros_treinamento/{id} deve retornar centro por ID"""
        # Arrange - Criar centro
        centro_data = {
            "nome": "CT King",
            "endereco": "Rua X, 123",
            "proprietario": "Marcos"
        }
        create_response = await client.post("/centros_treinamento/", json=centro_data)
        centro_id = create_response.json()["pk_id"]
        
        # Act
        response = await client.get(f"/centros_treinamento/{centro_id}")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "CT King"
        assert data["endereco"] == "Rua X, 123"
        assert data["proprietario"] == "Marcos"
        assert data["pk_id"] == centro_id
    
    @pytest.mark.asyncio
    async def test_get_centro_by_id_not_found(self, client: AsyncClient):
        """Teste: GET /centros_treinamento/{id} deve retornar 404 para ID inexistente"""
        # Act
        response = await client.get("/centros_treinamento/999")
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "Centro de treinamento com id 999 não encontrado" in data["detail"] 