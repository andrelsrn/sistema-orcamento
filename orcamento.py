import uuid  # Para gerar IDs únicos para os orçamentos


class Orcamento:
    def __init__(self, cliente, tipo_de_cerca, metragem, portao, valor_estimado):
        """
        Inicializa um novo orçamento.

        Parâmetros:
            cliente (Cliente): Objeto cliente ao qual o orçamento pertence.
            tipo_de_cerca (str): Descrição do tipo da cerca.
            metragem (float): Tamanho da cerca em metros.
            portao (bool): Indica se há portão (True/False).
            valor_estimado (float): Valor estimado para o orçamento.

        Levanta ValueError se algum dado obrigatório for inválido.
        """
        if not cliente or not tipo_de_cerca or metragem <= 0 or valor_estimado <= 0:
            raise ValueError(
                "Todos os campos são obrigatórios e devem ser válidos.")

        # Gerando um ID curto e único para o orçamento (8 caracteres)
        self.id = str(uuid.uuid4())[:8]

        self.cliente = cliente
        self.tipo_de_cerca = tipo_de_cerca
        self.metragem = metragem
        self.portao = portao
        self.valor_estimado = valor_estimado

        # Adiciona este orçamento à lista de orçamentos do cliente (associação bidirecional)
        cliente.orcamentos.append(self)

    def __str__(self):
        tem_portao = "Sim" if self.portao else "Não"
        return (
            f"Orçamento ID: {self.id} | "
            f"Cliente: {self.cliente.nome} (ID: {self.cliente.id}) | "
            f"Tipo de cerca: {self.tipo_de_cerca} | "
            f"Metragem: {self.metragem}m | "
            f"Portão: {tem_portao} | "
            f"Valor estimado: R$ {self.valor_estimado:.2f}"
        )
