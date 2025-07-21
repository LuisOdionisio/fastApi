import pytest
from pydantic import ValidationError
from workout_api.schemas.atleta_schema import AtletaIn, AtletaOut, AtletaUpdate
from workout_api.schemas.categoria_schema import CategoriaIn, CategoriaOut
from workout_api.schemas.centro_treinamento_schema import CentroTreinamentoIn, CentroTreinamentoOut

class TestAtletaSchema:
    """Testes para schemas do Atleta"""
    
    def test_atleta_in_valid_data(self):
        """Teste: AtletaIn deve aceitar dados válidos"""
        valid_data = {
            "nome": "João Silva",
            "cpf": "12345678901",
            "idade": 25,
            "peso": 75.5,
            "altura": 1.75,
            "sexo": "M",
            "categoria_id": 1,
            "centro_treinamento_id": 1
        }
        
        atleta = AtletaIn(**valid_data)
        
        assert atleta.nome == "João Silva"
        assert atleta.cpf == "12345678901"
        assert atleta.idade == 25
        assert atleta.peso == 75.5
        assert atleta.altura == 1.75
        assert atleta.sexo == "M"
        assert atleta.categoria_id == 1
        assert atleta.centro_treinamento_id == 1
    
    def test_atleta_in_invalid_cpf_with_letters(self):
        """Teste: AtletaIn deve rejeitar CPF com letras"""
        invalid_data = {
            "nome": "João Silva",
            "cpf": "1234567890a",
            "idade": 25,
            "peso": 75.5,
            "altura": 1.75,
            "sexo": "M",
            "categoria_id": 1,
            "centro_treinamento_id": 1
        }
        
        with pytest.raises(ValidationError) as exc_info:
            AtletaIn(**invalid_data)
        
        assert "CPF deve conter apenas números" in str(exc_info.value)
    
    def test_atleta_in_invalid_cpf_wrong_length(self):
        """Teste: AtletaIn deve rejeitar CPF com tamanho inválido"""
        invalid_data = {
            "nome": "João Silva",
            "cpf": "123456789",  # 9 dígitos, deveria ter 11
            "idade": 25,
            "peso": 75.5,
            "altura": 1.75,
            "sexo": "M",
            "categoria_id": 1,
            "centro_treinamento_id": 1
        }
        
        with pytest.raises(ValidationError):
            AtletaIn(**invalid_data)
    
    def test_atleta_in_invalid_sexo(self):
        """Teste: AtletaIn deve rejeitar sexo inválido"""
        invalid_data = {
            "nome": "João Silva",
            "cpf": "12345678901",
            "idade": 25,
            "peso": 75.5,
            "altura": 1.75,
            "sexo": "X",  # Deve ser M ou F
            "categoria_id": 1,
            "centro_treinamento_id": 1
        }
        
        with pytest.raises(ValidationError) as exc_info:
            AtletaIn(**invalid_data)
        
        assert "Sexo deve ser M ou F" in str(exc_info.value)
    
    def test_atleta_in_sexo_case_insensitive(self):
        """Teste: AtletaIn deve aceitar sexo em minúscula e converter para maiúscula"""
        valid_data = {
            "nome": "Maria Silva",
            "cpf": "12345678901",
            "idade": 25,
            "peso": 60.5,
            "altura": 1.65,
            "sexo": "f",  # minúscula
            "categoria_id": 1,
            "centro_treinamento_id": 1
        }
        
        atleta = AtletaIn(**valid_data)
        assert atleta.sexo == "F"
    
    def test_atleta_in_negative_idade(self):
        """Teste: AtletaIn deve rejeitar idade negativa"""
        invalid_data = {
            "nome": "João Silva",
            "cpf": "12345678901",
            "idade": -5,
            "peso": 75.5,
            "altura": 1.75,
            "sexo": "M",
            "categoria_id": 1,
            "centro_treinamento_id": 1
        }
        
        with pytest.raises(ValidationError):
            AtletaIn(**invalid_data)
    
    def test_atleta_in_negative_peso(self):
        """Teste: AtletaIn deve rejeitar peso negativo"""
        invalid_data = {
            "nome": "João Silva",
            "cpf": "12345678901",
            "idade": 25,
            "peso": -75.5,
            "altura": 1.75,
            "sexo": "M",
            "categoria_id": 1,
            "centro_treinamento_id": 1
        }
        
        with pytest.raises(ValidationError):
            AtletaIn(**invalid_data)
    
    def test_atleta_update_partial_data(self):
        """Teste: AtletaUpdate deve aceitar dados parciais"""
        update_data = {
            "nome": "João Santos",
            "idade": 26
        }
        
        atleta_update = AtletaUpdate(**update_data)
        
        assert atleta_update.nome == "João Santos"
        assert atleta_update.idade == 26

class TestCategoriaSchema:
    """Testes para schemas da Categoria"""
    
    def test_categoria_in_valid_data(self):
        """Teste: CategoriaIn deve aceitar dados válidos"""
        valid_data = {"nome": "Scale"}
        
        categoria = CategoriaIn(**valid_data)
        
        assert categoria.nome == "Scale"
    
    def test_categoria_in_empty_nome(self):
        """Teste: CategoriaIn deve rejeitar nome vazio"""
        invalid_data = {"nome": ""}
        
        with pytest.raises(ValidationError):
            CategoriaIn(**invalid_data)
    
    def test_categoria_out_with_id(self):
        """Teste: CategoriaOut deve incluir pk_id"""
        valid_data = {"pk_id": 1, "nome": "Scale"}
        
        categoria = CategoriaOut(**valid_data)
        
        assert categoria.pk_id == 1
        assert categoria.nome == "Scale"

class TestCentroTreinamentoSchema:
    """Testes para schemas do Centro de Treinamento"""
    
    def test_centro_treinamento_in_valid_data(self):
        """Teste: CentroTreinamentoIn deve aceitar dados válidos"""
        valid_data = {
            "nome": "CT King",
            "endereco": "Rua X, 123",
            "proprietario": "Marcos"
        }
        
        centro = CentroTreinamentoIn(**valid_data)
        
        assert centro.nome == "CT King"
        assert centro.endereco == "Rua X, 123"
        assert centro.proprietario == "Marcos"
    
    def test_centro_treinamento_in_empty_fields(self):
        """Teste: CentroTreinamentoIn deve rejeitar campos vazios"""
        invalid_data = {
            "nome": "",
            "endereco": "",
            "proprietario": ""
        }
        
        with pytest.raises(ValidationError):
            CentroTreinamentoIn(**invalid_data)
    
    def test_centro_treinamento_out_with_id(self):
        """Teste: CentroTreinamentoOut deve incluir pk_id"""
        valid_data = {
            "pk_id": 1,
            "nome": "CT King",
            "endereco": "Rua X, 123",
            "proprietario": "Marcos"
        }
        
        centro = CentroTreinamentoOut(**valid_data)
        
        assert centro.pk_id == 1
        assert centro.nome == "CT King"
        assert centro.endereco == "Rua X, 123"
        assert centro.proprietario == "Marcos" 