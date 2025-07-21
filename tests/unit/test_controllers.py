import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from workout_api.controllers.atleta_controller import AtletaController
from workout_api.controllers.categoria_controller import CategoriaController
from workout_api.controllers.centro_treinamento_controller import CentroTreinamentoController
from workout_api.schemas.atleta_schema import AtletaIn, AtletaUpdate
from workout_api.schemas.categoria_schema import CategoriaIn
from workout_api.schemas.centro_treinamento_schema import CentroTreinamentoIn
from tests.factories import AtletaFactory, CategoriaFactory, CentroTreinamentoFactory

class TestAtletaController:
    """Testes para AtletaController"""
    
    @pytest.mark.asyncio
    async def test_create_atleta_success(self):
        """Teste: Criar atleta com sucesso"""
        # Arrange
        mock_session = AsyncMock()
        atleta_in = AtletaIn(
            nome="João Silva",
            cpf="12345678901",
            idade=25,
            peso=75.5,
            altura=1.75,
            sexo="M",
            categoria_id=1,
            centro_treinamento_id=1
        )
        
        # Act
        result = await AtletaController.create(mock_session, atleta_in)
        
        # Assert
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()
        assert result is not None
    
    @pytest.mark.asyncio
    async def test_create_atleta_integrity_error(self):
        """Teste: Erro de integridade ao criar atleta com CPF duplicado"""
        # Arrange
        mock_session = AsyncMock()
        mock_session.commit.side_effect = IntegrityError("", "", "")
        
        atleta_in = AtletaIn(
            nome="João Silva",
            cpf="12345678901",
            idade=25,
            peso=75.5,
            altura=1.75,
            sexo="M",
            categoria_id=1,
            centro_treinamento_id=1
        )
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await AtletaController.create(mock_session, atleta_in)
        
        assert exc_info.value.status_code == 303
        assert "Já existe um atleta cadastrado com o cpf: 12345678901" in exc_info.value.detail
        mock_session.rollback.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_by_id_success(self):
        """Teste: Buscar atleta por ID com sucesso"""
        # Arrange
        mock_session = AsyncMock()
        mock_result = AsyncMock()
        mock_atleta = AtletaFactory.build()
        mock_result.scalar_one_or_none.return_value = mock_atleta
        mock_session.execute.return_value = mock_result
        
        # Act
        result = await AtletaController.get_by_id(mock_session, 1)
        
        # Assert
        assert result == mock_atleta
        mock_session.execute.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self):
        """Teste: Erro ao buscar atleta inexistente"""
        # Arrange
        mock_session = AsyncMock()
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await AtletaController.get_by_id(mock_session, 999)
        
        assert exc_info.value.status_code == 404
        assert "Atleta com id 999 não encontrado" in exc_info.value.detail
    
    @pytest.mark.asyncio
    async def test_update_atleta_success(self):
        """Teste: Atualizar atleta com sucesso"""
        # Arrange
        mock_session = AsyncMock()
        mock_result = AsyncMock()
        mock_atleta = AtletaFactory.build()
        mock_result.scalar_one_or_none.return_value = mock_atleta
        mock_session.execute.return_value = mock_result
        
        atleta_update = AtletaUpdate(nome="João Santos", idade=26)
        
        # Act
        result = await AtletaController.update(mock_session, 1, atleta_update)
        
        # Assert
        assert mock_atleta.nome == "João Santos"
        assert mock_atleta.idade == 26
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_delete_atleta_success(self):
        """Teste: Deletar atleta com sucesso"""
        # Arrange
        mock_session = AsyncMock()
        mock_result = AsyncMock()
        mock_atleta = AtletaFactory.build()
        mock_result.scalar_one_or_none.return_value = mock_atleta
        mock_session.execute.return_value = mock_result
        
        # Act
        await AtletaController.delete(mock_session, 1)
        
        # Assert
        mock_session.delete.assert_called_once_with(mock_atleta)
        mock_session.commit.assert_called_once()

class TestCategoriaController:
    """Testes para CategoriaController"""
    
    @pytest.mark.asyncio
    async def test_create_categoria_success(self):
        """Teste: Criar categoria com sucesso"""
        # Arrange
        mock_session = AsyncMock()
        categoria_in = CategoriaIn(nome="Scale")
        
        # Act
        result = await CategoriaController.create(mock_session, categoria_in)
        
        # Assert
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()
        assert result is not None
    
    @pytest.mark.asyncio
    async def test_create_categoria_integrity_error(self):
        """Teste: Erro de integridade ao criar categoria com nome duplicado"""
        # Arrange
        mock_session = AsyncMock()
        mock_session.commit.side_effect = IntegrityError("", "", "")
        categoria_in = CategoriaIn(nome="Scale")
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await CategoriaController.create(mock_session, categoria_in)
        
        assert exc_info.value.status_code == 303
        assert "Já existe uma categoria cadastrada com o nome: Scale" in exc_info.value.detail

class TestCentroTreinamentoController:
    """Testes para CentroTreinamentoController"""
    
    @pytest.mark.asyncio
    async def test_create_centro_success(self):
        """Teste: Criar centro de treinamento com sucesso"""
        # Arrange
        mock_session = AsyncMock()
        centro_in = CentroTreinamentoIn(
            nome="CT King",
            endereco="Rua X, 123",
            proprietario="Marcos"
        )
        
        # Act
        result = await CentroTreinamentoController.create(mock_session, centro_in)
        
        # Assert
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()
        assert result is not None
    
    @pytest.mark.asyncio
    async def test_create_centro_integrity_error(self):
        """Teste: Erro de integridade ao criar centro com nome duplicado"""
        # Arrange
        mock_session = AsyncMock()
        mock_session.commit.side_effect = IntegrityError("", "", "")
        centro_in = CentroTreinamentoIn(
            nome="CT King",
            endereco="Rua X, 123",
            proprietario="Marcos"
        )
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await CentroTreinamentoController.create(mock_session, centro_in)
        
        assert exc_info.value.status_code == 303
        assert "Já existe um centro de treinamento cadastrado com o nome: CT King" in exc_info.value.detail 