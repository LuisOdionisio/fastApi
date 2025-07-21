from fastapi import FastAPI
from fastapi_pagination import add_pagination
from workout_api.routers import atleta_router, categoria_router, centro_treinamento_router

app = FastAPI(
    title='WorkOut API',
    description='API para gerenciamento de academia de CrossFit',
    version='1.0.0'
)

app.include_router(
    atleta_router.router, 
    prefix='/atletas', 
    tags=['atletas']
)
app.include_router(
    categoria_router.router, 
    prefix='/categorias', 
    tags=['categorias']
)
app.include_router(
    centro_treinamento_router.router, 
    prefix='/centros_treinamento', 
    tags=['centros_treinamento']
)

# Configurar paginação
add_pagination(app) 