import factory
from datetime import datetime
from workout_api.models.atleta_model import AtletaModel
from workout_api.models.categoria_model import CategoriaModel
from workout_api.models.centro_treinamento_model import CentroTreinamentoModel

class CategoriaFactory(factory.Factory):
    class Meta:
        model = CategoriaModel
    
    pk_id = factory.Sequence(lambda n: n)
    nome = factory.Faker('word')

class CentroTreinamentoFactory(factory.Factory):
    class Meta:
        model = CentroTreinamentoModel
    
    pk_id = factory.Sequence(lambda n: n)
    nome = factory.Faker('company')
    endereco = factory.Faker('address')
    proprietario = factory.Faker('name')

class AtletaFactory(factory.Factory):
    class Meta:
        model = AtletaModel
    
    pk_id = factory.Sequence(lambda n: n)
    nome = factory.Faker('name')
    cpf = factory.Faker('numerify', text='###########')
    idade = factory.Faker('random_int', min=18, max=45)
    peso = factory.Faker('pyfloat', positive=True, min_value=50.0, max_value=120.0)
    altura = factory.Faker('pyfloat', positive=True, min_value=1.50, max_value=2.20)
    sexo = factory.Faker('random_element', elements=['M', 'F'])
    created_at = factory.LazyFunction(datetime.utcnow)
    categoria_id = 1
    centro_treinamento_id = 1 