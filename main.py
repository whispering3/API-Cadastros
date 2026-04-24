from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import time
from sqlalchemy.exc import OperationalError
from fastapi.staticfiles import StaticFiles
from routers import user_router, auth_router, order_router
from core.config import settings
from database import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Tenta criar as tabelas com retentativas caso o banco ainda esteja iniciando
    retries = 5
    while retries > 0:
        try:
            Base.metadata.create_all(bind=engine)
            break
        except OperationalError:
            retries -= 1
            print(f"Banco de dados não disponível. Retentando em 5 segundos... ({retries} tentativas restantes)")
            time.sleep(5)
    yield

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="API de gestão de clientes e pedidos com autenticação JWT e Soft Delete.",
    lifespan=lifespan
)

# Monta o diretório frontend para servir arquivos estáticos
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/", tags=["Dashboard"])
def read_index():
    from fastapi.responses import FileResponse
    return FileResponse("frontend/index.html")


# CORS para permitir acesso do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusão das rotas
app.include_router(auth_router.router, prefix=f"{settings.API_STR}/auth", tags=["Autenticação"])
app.include_router(user_router.router, prefix=f"{settings.API_STR}/users", tags=["Usuários"])
app.include_router(order_router.router, prefix=f"{settings.API_STR}/orders", tags=["Pedidos"])

@app.get("/", tags=["Health Check"])
def root():
    return {"message": "API de Gestão de Clientes está online!", "docs": "/docs"}
