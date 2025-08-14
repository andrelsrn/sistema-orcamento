from cliente import Cliente
from orcamento import Orcamento
import re  # Importa o módulo de expressões regulares para validação


class SistemaOrcamento:
    def __init__(self):
        """
        Inicializa o sistema, criando listas vazias para clientes e orçamentos,
        além de um contador para gerar IDs únicos para clientes.
        """
        self.clientes = []
        self.orcamentos = []
        self.proximo_id_cliente = 1

    def cadastrar_cliente(self, nome, telefone, endereco, email):
        """
        Cria e adiciona um novo cliente à lista, gerando um ID único.
        Verifica se todos os campos obrigatórios foram preenchidos.
        Retorna o objeto Cliente criado.
        """
        if not nome or not telefone or not endereco or not email:
            raise ValueError("Todos os campos são obrigatórios.")

        cliente = Cliente(nome, self.proximo_id_cliente,
                          telefone, endereco, email)
        self.clientes.append(cliente)
        self.proximo_id_cliente += 1
        return cliente

    def cadastrar_orcamento(self, cliente_id, metragem, portao, valor_estimado, material, t_painel, cor_material):
        """
        Busca o cliente pelo ID fornecido.
        Se existir, cria um orçamento associado ao cliente e adiciona à lista.
        Retorna o objeto Orcamento criado.
        """
        cliente = next((c for c in self.clientes if c.id == cliente_id), None)
        if not cliente:
            raise ValueError("Cliente não encontrado.")

        orcamento = Orcamento(cliente, metragem, portao,
                              valor_estimado, material, t_painel, cor_material)
        self.orcamentos.append(orcamento)

        # Associa o orçamento ao cliente (responsabilidade do sistema)
        cliente.orcamentos.append(orcamento)
        return orcamento

    def listar_orcamentos(self):
        """
        Retorna a lista de todos os orçamentos cadastrados.
        """
        return self.orcamentos

    def consultar_orcamento_por_nome(self, nome_cliente):
        """
        Busca orçamentos relacionados ao cliente com o nome fornecido.
        Se não encontrar, lança um erro.
        Retorna a lista de orçamentos encontrados.
        """
        orcamentos_encontrados = [
            orc for orc in self.orcamentos if orc.cliente.nome.lower() == nome_cliente.lower()]
        if not orcamentos_encontrados:
            raise ValueError(
                "Nenhum orçamento encontrado para o cliente informado.")
        return orcamentos_encontrados

    def listar_clientes(self):
        """
        Retorna a lista de todos os clientes cadastrados.
        """
        return self.clientes

    def buscar_cliente_por_nome(self, nome):
        """
        Retorna uma lista com todos os clientes que possuem o nome exatamente igual (case insensitive).
        """
        return [c for c in self.clientes if c.nome.lower() == nome.lower()]

    def atualizar_cliente(self, cliente_id, nome=None, telefone=None, endereco=None, email=None):
        """
        Atualiza os dados do cliente que possuir o ID informado.
        Apenas os campos fornecidos são atualizados.
        """
        cliente = next((c for c in self.clientes if c.id == cliente_id), None)
        if not cliente:
            raise ValueError("Cliente não encontrado para atualização.")

        # Atualiza cada campo apenas se um novo valor for fornecido
        if nome is not None:
            nome = nome.strip()
            if not nome or not nome.replace(" ", "").isalpha():
                raise ValueError("Nome inválido. Deve conter apenas letras.")
            cliente.nome = nome

        if telefone is not None:
            telefone = telefone.strip()
            if not re.match(r"^\d{11}$", telefone):
                raise ValueError(
                    "Telefone deve conter exatamente 11 números (com DDD).")
            cliente.telefone = telefone

        if endereco is not None:
            endereco = endereco.strip()
            if not endereco:
                raise ValueError("Endereço não pode ser vazio.")
            cliente.endereco = endereco

        if email is not None:
            email = email.strip()
            if not re.fullmatch(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
                raise ValueError("Formato de Email inválido.")
            cliente.email = email

        return cliente
