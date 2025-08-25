import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.base import Base
from src.models import Cliente
from src.services.cliente_service import cadastrar_cliente, listar_clientes, buscar_cliente_por_nome, atualizar_cliente, deletar_cliente

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

def test_listar_clientes_vazio(db_session):
    # ARRANGE - No clients added
    # ACT
    clientes = listar_clientes(db=db_session)
    # ASSERT
    assert len(clientes) == 0

def test_listar_clientes_com_dados(db_session):
    # ARRANGE
    cadastrar_cliente("Cliente 1", "11111111111", "End 1", "email1@test.com", db=db_session)
    cadastrar_cliente("Cliente 2", "22222222222", "End 2", "email2@test.com", db=db_session)
    # ACT
    clientes = listar_clientes(db=db_session)
    # ASSERT
    assert len(clientes) == 2
    assert clientes[0].nome == "Cliente 1"
    assert clientes[1].nome == "Cliente 2"

def test_buscar_cliente_por_nome_encontrado(db_session):
    # ARRANGE
    cadastrar_cliente("Alice Silva", "11111111111", "Rua A", "alice@test.com", db=db_session)
    cadastrar_cliente("Bob Santos", "22222222222", "Rua B", "bob@test.com", db=db_session)
    # ACT
    clientes_encontrados = buscar_cliente_por_nome("Alice", db=db_session)
    # ASSERT
    assert len(clientes_encontrados) == 1
    assert clientes_encontrados[0].nome == "Alice Silva"

def test_buscar_cliente_por_nome_nao_encontrado(db_session):
    # ARRANGE
    cadastrar_cliente("Alice Silva", "11111111111", "Rua A", "alice@test.com", db=db_session)
    # ACT
    clientes_encontrados = buscar_cliente_por_nome("Carlos", db=db_session)
    # ASSERT
    assert len(clientes_encontrados) == 0

def test_atualizar_cliente_com_sucesso(db_session):
    # ARRANGE
    cliente_original = cadastrar_cliente("Cliente Antigo", "11111111111", "End Antigo", "antigo@test.com", db=db_session)
    # ACT
    cliente_atualizado = atualizar_cliente(
        cliente_id=cliente_original.id,
        nome="Cliente Novo",
        telefone="99999999999",
        db=db_session
    )
    # ASSERT
    assert cliente_atualizado.nome == "Cliente Novo"
    assert cliente_atualizado.telefone == "99999999999"
    assert cliente_atualizado.endereco == "End Antigo" # Should remain unchanged
    assert cliente_atualizado.email == "antigo@test.com" # Should remain unchanged

def test_atualizar_cliente_nao_encontrado(db_session):
    # ARRANGE - No client with ID 999
    # ACT & ASSERT
    with pytest.raises(ValueError, match="Cliente não encontrado para atualização."):
        atualizar_cliente(cliente_id=999, nome="Inexistente", db=db_session)

def test_deletar_cliente_com_sucesso(db_session):
    # ARRANGE
    cliente_para_deletar = cadastrar_cliente("Cliente X", "11111111111", "End X", "x@test.com", db=db_session)
    # ACT
    resultado = deletar_cliente(cliente_id=cliente_para_deletar.id, db=db_session)
    # ASSERT
    assert resultado is True
    clientes_restantes = listar_clientes(db=db_session)
    assert len(clientes_restantes) == 0

def test_deletar_cliente_nao_encontrado(db_session):
    # ARRANGE - No client with ID 999
    # ACT & ASSERT
    with pytest.raises(ValueError, match="Cliente não encontrado para exclusão."):
        deletar_cliente(cliente_id=999, db=db_session)
