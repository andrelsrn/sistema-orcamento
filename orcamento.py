import uuid  # Para gerar IDs únicos para os orçamentos


class Orcamento:
    def __init__(self, cliente, tipo_de_cerca, metragem, portao, valor_estimado, material, t_painel, cor):
        """
        Inicializa um novo orçamento.
        """
        # Validações de campos obrigatórios
        if not cliente:
            raise ValueError("Cliente inválido.")
        if not tipo_de_cerca.strip():
            raise ValueError("Tipo de cerca é obrigatório.")
        if metragem <= 0:
            raise ValueError("Metragem deve ser maior que zero.")
        if valor_estimado <= 0:
            raise ValueError("Valor estimado deve ser maior que zero.")
        if not material.strip():
            raise ValueError("Material é obrigatório.")
        if not t_painel.strip():
            raise ValueError("Tamanho do painel é obrigatório.")
        if not cor.strip():
            raise ValueError("Cor é obrigatória.")

        # ID único (8 caracteres)
        self.id = str(uuid.uuid4())[:8]

        # Atributos do orçamento
        self.cliente = cliente
        self.tipo_de_cerca = tipo_de_cerca
        self.metragem = metragem
        self.portao = portao
        self.valor_estimado = valor_estimado
        self.material = material
        self.t_painel = t_painel
        self.cor = cor

        # Associa o orçamento ao cliente
        cliente.orcamentos.append(self)

    def __str__(self):
        tem_portao = "Sim" if self.portao else "Não"
        return (
            f"Orçamento ID: {self.id} | "
            f"Cliente: {self.cliente.nome} (ID: {self.cliente.id}) | "
            f"Material: {self.material} | "
            f"Tamanho Painel: {self.t_painel} | "
            f"Cor: {self.cor} | "
            f"Metragem: {self.metragem}m | "
            f"Portão: {tem_portao} | "
            f"Valor estimado: R$ {self.valor_estimado:.2f}"
        )
