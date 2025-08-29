import json
from sqlalchemy.orm import joinedload, Session
from ..models import Cliente, Orcamento
from ..valores import TABELA_PRECOS, VALOR_PORTAO


def calcular_valor_estimado(metragem, material, t_painel, cor_material, portao, qnt_portao):
    """Calcula o valor estimado do orçamento com base nos materiais e metragem."""
    chave_preco = (material, t_painel, cor_material) if material == 'pvc' else (
        material, t_painel)

    preco_metro = TABELA_PRECOS.get(chave_preco)
    if preco_metro is None:
        raise ValueError(
            f"Combinação de material '{material}', painel '{t_painel}' e cor '{cor_material}' não encontrada.")

    valor_total = preco_metro * metragem
    if portao and qnt_portao and qnt_portao > 0:
        valor_total += VALOR_PORTAO * qnt_portao

    return valor_total


def cadastrar_orcamento(cliente_id, metragem, portao, material, t_painel, cor_material,
                        tamanho_portao, qnt_portao, portoes, db: Session):
    try:
        cliente = db.query(Cliente).filter(
            Cliente.id == cliente_id).first()
        if not cliente:
            raise ValueError("Cliente não encontrado.")

        valor_estimado = calcular_valor_estimado(
            metragem, material, t_painel, cor_material, portao, qnt_portao)

        orcamento = Orcamento(
            cliente_id=cliente.id,
            metragem=metragem,
            portao=True if portao == 'sim' else False,
            valor_estimado=valor_estimado,
            material=material,
            t_painel=t_painel,
            cor_material=cor_material,
            tamanho_portao=tamanho_portao,
            qnt_portao=qnt_portao,
            portoes=json.dumps(portoes)
        )

        db.add(orcamento)
        db.commit()
        db.refresh(orcamento)
        # Para evitar o DetachedInstanceError, buscamos o objeto recém-criado
        # novamente, desta vez usando joinedload para carregar o cliente junto.
        orcamento_completo = db.query(Orcamento).options(
            joinedload(Orcamento.cliente)
        ).filter(Orcamento.id == orcamento.id).one()
        return orcamento_completo

    except Exception as e:
        db.rollback()
        raise e


def listar_orcamentos(db: Session):
    return db.query(Orcamento).options(joinedload(Orcamento.cliente)).all()


def consultar_orcamento_por_nome(nome_cliente: str, db: Session):
    orcamentos = (
        db.query(Orcamento)
        .options(joinedload(Orcamento.cliente))
        .join(Cliente)
        .filter(Cliente.nome.ilike(f"%{nome_cliente}%"))
        .all()
    )
    if not orcamentos:
        raise ValueError(
            "Nenhum orçamento encontrado para o cliente informado.")
    return orcamentos


def consultar_orcamento_por_id(orcamento_id: int, db: Session):
    '''Consulta um orçamento pelo ID, incluindo os dados do cliente.'''
    return db.query(Orcamento).options(joinedload(Orcamento.cliente)).filter(Orcamento.id == orcamento_id).first()
