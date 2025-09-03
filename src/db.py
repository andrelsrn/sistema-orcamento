"""Configura a conexão com o banco de dados e a sessão do SQLAlchemy."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./orcamentos.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}  # Necessário para SQLite com múltiplos threads (FastAPI, etc.)
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
