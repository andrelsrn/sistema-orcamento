import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.base import Base
from src.models import Cliente
from src.services.cliente_service import cadastrar_cliente

# Passo 1: Configuração do banco de dados de teste
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

# Passo 2: Teste completo
def test_cadastrar_cliente_com_sucesso(db_session):
    # ARRANGE
    nome_teste = "John McDonalds"
    telefone_teste = "11999999999"
    endereco_teste = "Teste St, 35"
    email_teste = "teste@exemplo.com"

    # ACT
    cliente_cadastrado = cadastrar_cliente(
        nome=nome_teste,
        telefone=telefone_teste,
        endereco=endereco_teste,
        email=email_teste,
        db=db_session
    )

    # ASSERT
    assert cliente_cadastrado is not None
    assert cliente_cadastrado.id is not None
    assert cliente_cadastrado.nome == nome_teste
    assert cliente_cadastrado.email == email_teste