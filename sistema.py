from cliente import Cliente
from orcamento import Orcamento


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

        cliente = Cliente(nome, self.proximo_id_cliente,telefone, endereco, email)
        self.clientes.append(cliente)
        self.proximo_id_cliente += 1
        return cliente

    def cadastrar_orcamento(self, cliente_id, tipo_de_cerca, metragem, portao, valor_estimado, material, t_painel, cor):
        """
        Busca o cliente pelo ID fornecido.
        Se existir, cria um orçamento associado ao cliente e adiciona à lista.
        Retorna o objeto Orcamento criado.
        """
        cliente = next((c for c in self.clientes if c.id == cliente_id), None)
        if not cliente:
            raise ValueError("Cliente não encontrado.")

        orcamento = Orcamento(cliente, tipo_de_cerca,metragem, portao, valor_estimado, material, t_painel,cor)
        self.orcamentos.append(orcamento)
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
