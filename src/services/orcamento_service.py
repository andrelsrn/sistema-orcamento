import json
from sqlalchemy.orm import joinedload, Session
from ..models import Cliente, Orcamento
from ..config import TABELA_PRECOS, VALOR_PORTAO




def calcular_valor_estimado(metragem, material, t_painel, cor_material, portao, qnt_portao):
    """Calcula o valor estimado do orçamento com base nos materiais e metragem."""
    
    # O preço do PVC varia por cor, enquanto outros materiais não.
    if material.lower() == 'pvc':
        chave_preco = (material.lower(), t_painel, cor_material.lower())
    else:
        chave_preco = (material.lower(), t_painel)

    preco_metro = TABELA_PRECOS.get(chave_preco)
    
    if preco_metro is None:
        raise ValueError(
            f"Combinação de material '{chave_preco[0]}', painel '{chave_preco[1]}' e cor '{chave_preco[2] if len(chave_preco) > 2 else '-'}' não foi encontrada na tabela de preços.")

    valor_total = preco_metro * metragem
    if portao and qnt_portao and qnt_portao > 0:
        valor_total += VALOR_PORTAO * qnt_portao

    return valor_total


def cadastrar_orcamento(cliente_id, metragem, portao, material, t_painel, cor_material,
                        tamanho_portao, qnt_portao, portoes, db: Session):
    """Cadastra um novo orçamento no banco de dados.

    Calcula o valor estimado, associa ao cliente e salva o registro.
    Os detalhes dos portões são recebidos como um dicionário e salvos como JSON.

    Args:
        cliente_id (int): ID do cliente ao qual o orçamento pertence.
        metragem (float): A metragem total da cerca.
        portao (str): 'sim' ou 'não', indicando a presença de portão.
        material (str): O material principal da cerca.
        t_painel (str): O tamanho do painel.
        cor_material (str | None): A cor, aplicável apenas para PVC.
        tamanho_portao (str | None): O tamanho do portão.
        qnt_portao (int): A quantidade de portões.
        portoes (dict): Um dicionário com detalhes dos portões.
        db (Session): A sessão do SQLAlchemy para interagir com o banco.

    Returns:
        Orcamento: O objeto Orcamento completo, com os dados do cliente.
    """
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
    """Lista todos os orçamentos registrados, incluindo os dados dos clientes."""
    return db.query(Orcamento).options(joinedload(Orcamento.cliente)).all()


def consultar_orcamento_por_nome(nome_cliente: str, db: Session):
    """Consulta orçamentos pelo nome do cliente, permitindo buscas parciais."""
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
