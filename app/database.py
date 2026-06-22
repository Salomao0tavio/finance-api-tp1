"""
Configuração da conexão com o banco de dados.
Usa SQLite por padrão, mas pode ser sobrescrito via variável de ambiente DATABASE_URL.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./finance.db")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency do FastAPI para obter uma sessão de banco de dados por request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
