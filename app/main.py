"""Ponto de entrada da aplicação FastAPI."""
from fastapi import FastAPI

from app.database import Base, engine
from app.routers import user_router, account_router, category_router, transaction_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Finance API",
    description="API de Controle de Gastos Pessoais — Trabalho Prático de GCS",
    version="1.0.0",
)

app.include_router(user_router)
app.include_router(account_router)
app.include_router(category_router)
app.include_router(transaction_router)


@app.get("/health", tags=["health"])
def health_check():
    """Endpoint de healthcheck, usado pelo pipeline de deploy para validar a aplicação."""
    return {"status": "ok"}
