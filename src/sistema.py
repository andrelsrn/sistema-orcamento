from .db import SessionLocal
from .models import Cliente, Orcamento
import re
from .services.cliente_service import (
    cadastrar_cliente,
    listar_clientes,
    buscar_cliente_por_nome,
    atualizar_cliente,
    deletar_cliente
)
from .services.orcamento_service import (
    cadastrar_orcamento,
    consultar_orcamento_por_nome,
    listar_orcamentos
)


class SistemaOrcamento:
    def __init__(self):
        """
        Inicializa o sistema.
        Agora os clientes e orçamentos são gerenciados via banco de dados,
        usando os services correspondentes.
        """

    def cadastrar_cliente(self, nome, telefone, endereco, email):
        with SessionLocal() as session:
            if not nome or not telefone or not endereco or not email:
                raise ValueError("Todos os campos são obrigatórios.")
            
            cliente = cadastrar_cliente(nome, telefone, endereco, email, db=session)
            return cliente

    def cadastrar_orcamento(self, cliente_id, metragem, portao, material, t_painel, cor_material, tamanho_portao, qnt_portao, portoes):
        with SessionLocal() as session:
            return cadastrar_orcamento(cliente_id, metragem, portao,
                                       material, t_painel, cor_material, tamanho_portao, qnt_portao, portoes, db=session)

    def listar_orcamentos(self):
        with SessionLocal() as session:
            return listar_orcamentos(db=session)

    def consultar_orcamento_por_nome(self, nome_cliente):
        with SessionLocal() as session:
            return consultar_orcamento_por_nome(nome_cliente, db=session)

    def listar_clientes(self):
        with SessionLocal() as session:
            return listar_clientes(db=session)

    def buscar_cliente_por_nome(self, nome):
        with SessionLocal() as session:
            return buscar_cliente_por_nome(nome, db=session)

    def atualizar_cliente(self, cliente_id, nome=None, telefone=None, endereco=None, email=None):
        with SessionLocal() as session:
            return atualizar_cliente(cliente_id, nome, telefone, endereco, email, db=session)

    def deletar_cliente(self, cliente_id):
        with SessionLocal() as session:
            return deletar_cliente(cliente_id, db=session)