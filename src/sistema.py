from models.cliente import Cliente
from models.orcamento import Orcamento
import re  # Importa o módulo de expressões regulares para validação
from services.cliente_service import (
    cadastrar_cliente,
    listar_clientes,
    buscar_cliente_por_nome,
    atualizar_cliente,
    deletar_cliente
)
from services.orcamento_service import cadastrar_orcamento, consultar_orcamento_por_nome, listar_orcamentos


class SistemaOrcamento:
    def __init__(self):
        """
        Inicializa o sistema.
        Agora os clientes e orçamentos são gerenciados via banco de dados,
        usando os services correspondentes.
        """

    def cadastrar_cliente(self, nome, telefone, endereco, email):

        if not nome or not telefone or not endereco or not email:
            raise ValueError("Todos os campos são obrigatórios.")
        # Chama o service que salva no banco e retorna o cliente
        cliente = cadastrar_cliente(nome, telefone, endereco, email)
        return (cliente)

    def cadastrar_orcamento(self, cliente_id, metragem, portao, material, t_painel, cor_material, tamanho_portao, qnt_portao, portoes):
        return cadastrar_orcamento(cliente_id, metragem, portao,
                                   material, t_painel, cor_material, tamanho_portao, qnt_portao, portoes)

    def listar_orcamentos(self):
        return listar_orcamentos()

    def consultar_orcamento_por_nome(self, nome_cliente):
        return consultar_orcamento_por_nome(nome_cliente)

    def listar_clientes(self):
        return listar_clientes()

    def buscar_cliente_por_nome(self, nome):
        return buscar_cliente_por_nome(nome)

    def atualizar_cliente(self, cliente_id, nome=None, telefone=None, endereco=None, email=None):
        return atualizar_cliente(cliente_id, nome, telefone, endereco, email)

    def deletar_cliente(self, cliente_id):
        return deletar_cliente(cliente_id)
