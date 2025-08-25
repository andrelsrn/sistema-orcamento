import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.base import Base
from src.models import Cliente, Orcamento
from src.services.cliente_service import cadastrar_cliente
from src.services.orcamento_service import (
    calcular_valor_estimado,
    cadastrar_orcamento,
    listar_orcamentos,
    consultar_orcamento_por_nome
)

# Configuração do banco de dados de teste em memória
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

# Testes para calcular_valor_estimado
def test_calcular_valor_estimado_madeira(db_session):
    valor = calcular_valor_estimado(metragem=10, material="madeira", t_painel="6x6", cor_material=None, portao=False, qnt_portao=0)
    assert valor == 19 * 10

def test_calcular_valor_estimado_pvc_com_cor(db_session):
    valor = calcular_valor_estimado(metragem=5, material="pvc", t_painel="6x6", cor_material="branco", portao=False, qnt_portao=0)
    assert valor == 25 * 5

def test_calcular_valor_estimado_com_portao(db_session):
    valor = calcular_valor_estimado(metragem=10, material="madeira", t_painel="6x6", cor_material=None, portao=True, qnt_portao=1)
    assert valor == (19 * 10) + 250.00

def test_calcular_valor_estimado_combinacao_invalida(db_session):
    with pytest.raises(ValueError, match="Combinação de material 'material_invalido'"): # Adjusted match
        calcular_valor_estimado(metragem=10, material="material_invalido", t_painel="6x6", cor_material=None, portao=False, qnt_portao=0)

# Testes para cadastrar_orcamento
def test_cadastrar_orcamento_com_sucesso(db_session: Session):
    cliente = cadastrar_cliente("Cliente Teste", "11987654321", "Rua Teste", "teste@email.com", db=db_session)
    orcamento = cadastrar_orcamento(
        cliente_id=cliente.id,
        metragem=10,
        portao=False,
        material="madeira",
        t_painel="6x6",
        cor_material=None,
        tamanho_portao=None,
        qnt_portao=0,
        portoes={},
        db=db_session
    )
    assert orcamento is not None
    assert orcamento.cliente_id == cliente.id
    assert orcamento.valor_estimado == 190.00

def test_cadastrar_orcamento_cliente_nao_encontrado(db_session: Session):
    with pytest.raises(ValueError, match="Cliente não encontrado."):
        cadastrar_orcamento(
            cliente_id=999,
            metragem=10,
            portao=False,
            material="madeira",
            t_painel="6x6",
            cor_material=None,
            tamanho_portao=None,
            qnt_portao=0,
            portoes={},
            db=db_session
        )

# Testes para listar_orcamentos
def test_listar_orcamentos_vazio(db_session: Session):
    orcamentos = listar_orcamentos(db=db_session)
    assert len(orcamentos) == 0

def test_listar_orcamentos_com_dados(db_session: Session):
    cliente = cadastrar_cliente("Cliente List", "11111111111", "End List", "list@email.com", db=db_session)
    cadastrar_orcamento(
        cliente_id=cliente.id,
        metragem=10,
        portao=False,
        material="madeira",
        t_painel="6x6",
        cor_material=None,
        tamanho_portao=None,
        qnt_portao=0,
        portoes={},
        db=db_session
    )
    orcamentos = listar_orcamentos(db=db_session)
    assert len(orcamentos) == 1
    assert orcamentos[0].cliente.nome == "Cliente List"

# Testes para consultar_orcamento_por_nome
def test_consultar_orcamento_por_nome_encontrado(db_session: Session):
    cliente = cadastrar_cliente("Cliente Busca", "11223344556", "Rua Busca", "busca@email.com", db=db_session)
    cadastrar_orcamento(
        cliente_id=cliente.id,
        metragem=10,
        portao=False,
        material="madeira",
        t_painel="6x6",
        cor_material=None,
        tamanho_portao=None,
        qnt_portao=0,
        portoes={},
        db=db_session
    )
    orcamentos_encontrados = consultar_orcamento_por_nome("Cliente Busca", db=db_session)
    assert len(orcamentos_encontrados) == 1
    assert orcamentos_encontrados[0].cliente.nome == "Cliente Busca"

def test_consultar_orcamento_por_nome_nao_encontrado(db_session: Session):
    with pytest.raises(ValueError, match="Nenhum orçamento encontrado para o cliente informado."):
        consultar_orcamento_por_nome("Cliente Inexistente", db=db_session)
