import json
from sqlalchemy.orm import joinedload
from db import SessionLocal
from models.cliente import Cliente
from models.orcamento import Orcamento

# Tabela de preços movida para o service, onde a lógica de negócio reside.
tabela_precos = {
    ("madeira", "6x6"): 19,
    ("madeira", "6x8"): 18,
    ("aluminio", "5x5"): 24,
    ("aluminio", "4x5"): 25,
    ("pvc", "6x6", "branco"): 25,
    ("pvc", "6x6", "bege"): 26,
    ("pvc", "6x6", "marrom"): 47,
    ("pvc", "6x6", "cinza"): 48,
    ("pvc", "6x8", "branco"): 27,
    ("pvc", "6x8", "bege"): 28,
    ("pvc", "6x8", "marrom"): 49,
    ("pvc", "6x8", "cinza"): 50
}
valor_portao = 250.00

def calcular_valor_estimado(metragem, material, t_painel, cor_material, portao, qnt_portao):
    """Calcula o valor estimado do orçamento com base nos materiais e metragem."""
    chave_preco = (material, t_painel, cor_material) if material == 'pvc' else (material, t_painel)
    
    preco_metro = tabela_precos.get(chave_preco)
    if preco_metro is None:
        raise ValueError(f"Combinação de material '{material}', painel '{t_painel}' e cor '{cor_material}' não encontrada.")

    valor_total = preco_metro * metragem
    if portao and qnt_portao and qnt_portao > 0:
        valor_total += valor_portao * qnt_portao
        
    return valor_total

def cadastrar_orcamento(cliente_id, metragem, portao, material, t_painel, cor_material,
                        tamanho_portao, qnt_portao, portoes):
    with SessionLocal() as session:
        try:
            cliente = session.query(Cliente).filter(Cliente.id == cliente_id).first()
            if not cliente:
                raise ValueError("Cliente não encontrado.")

            # Lógica de cálculo do valor estimado foi movida para cá
            valor_estimado = calcular_valor_estimado(metragem, material, t_painel, cor_material, portao, qnt_portao)

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
                portoes=json.dumps(portoes) # Converte o dicionário de portões para uma string JSON
            )

            session.add(orcamento)
            session.commit()
            
            # Para evitar o DetachedInstanceError, buscamos o objeto recém-criado
            # novamente, desta vez usando joinedload para carregar o cliente junto.
            orcamento_completo = session.query(Orcamento).options(
                joinedload(Orcamento.cliente)
            ).filter(Orcamento.id == orcamento.id).one()

            return orcamento_completo

        except Exception as e:
            session.rollback()
            raise e

def listar_orcamentos():
    with SessionLocal() as session:
        return session.query(Orcamento).options(joinedload(Orcamento.cliente)).all()

def consultar_orcamento_por_nome(nome_cliente: str):
    with SessionLocal() as session:
        orcamentos = (
            session.query(Orcamento)
            .options(joinedload(Orcamento.cliente))
            .join(Cliente)
            .filter(Cliente.nome.ilike(f"%{nome_cliente}%"))
            .all()
        )
        if not orcamentos:
            raise ValueError(
                "Nenhum orçamento encontrado para o cliente informado.")
        return orcamentos
