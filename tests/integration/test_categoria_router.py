import pytest
from httpx import AsyncClient

class TestCategoriaRouter:
    """Testes de integração para rotas de categoria"""
    
    @pytest.mark.asyncio
    async def test_create_categoria_success(self, client: AsyncClient):
        """Teste: POST /categorias deve criar categoria com sucesso"""
        # Arrange
        categoria_data = {"nome": "Scale"}
        
        # Act
        response = await client.post("/categorias/", json=categoria_data)
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["nome"] == "Scale"
        assert "pk_id" in data
    
    @pytest.mark.asyncio
    async def test_create_categoria_duplicate_name(self, client: AsyncClient):
        """Teste: POST /categorias deve falhar com nome duplicado"""
        # Arrange - Criar primeira categoria
        categoria_data = {"nome": "Scale"}
        await client.post("/categorias/", json=categoria_data)
        
        # Act - Tentar criar segunda categoria com mesmo nome
        response = await client.post("/categorias/", json=categoria_data)
        
        # Assert
        assert response.status_code == 303
        data = response.json()
        assert "Já existe uma categoria cadastrada com o nome: Scale" in data["detail"]
    
    @pytest.mark.asyncio
    async def test_create_categoria_invalid_data(self, client: AsyncClient):
        """Teste: POST /categorias deve falhar com dados inválidos"""
        # Arrange
        invalid_data = {"nome": ""}
        
        # Act
        response = await client.post("/categorias/", json=invalid_data)
        
        # Assert
        assert response.status_code == 422
    
    @pytest.mark.asyncio
    async def test_get_categorias_empty(self, client: AsyncClient):
        """Teste: GET /categorias deve retornar lista vazia quando não há categorias"""
        # Act
        response = await client.get("/categorias/")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data == []
    
    @pytest.mark.asyncio
    async def test_get_categorias_with_data(self, client: AsyncClient):
        """Teste: GET /categorias deve retornar lista de categorias"""
        # Arrange - Criar categorias
        categoria1_data = {"nome": "Scale"}
        categoria2_data = {"nome": "RX"}
        
        await client.post("/categorias/", json=categoria1_data)
        await client.post("/categorias/", json=categoria2_data)
        
        # Act
        response = await client.get("/categorias/")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        nomes = [categoria["nome"] for categoria in data]
        assert "Scale" in nomes
        assert "RX" in nomes
    
    @pytest.mark.asyncio
    async def test_get_categoria_by_id_success(self, client: AsyncClient):
        """Teste: GET /categorias/{id} deve retornar categoria por ID"""
        # Arrange - Criar categoria
        categoria_data = {"nome": "Scale"}
        create_response = await client.post("/categorias/", json=categoria_data)
        categoria_id = create_response.json()["pk_id"]
        
        # Act
        response = await client.get(f"/categorias/{categoria_id}")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "Scale"
        assert data["pk_id"] == categoria_id
    
    @pytest.mark.asyncio
    async def test_get_categoria_by_id_not_found(self, client: AsyncClient):
        """Teste: GET /categorias/{id} deve retornar 404 para ID inexistente"""
        # Act
        response = await client.get("/categorias/999")
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "Categoria com id 999 não encontrada" in data["detail"] 