import uuid  # Para gerar IDs únicos para os orçamentos


class Orcamento:
    def __init__(self, cliente, metragem, portao, valor_estimado, material, t_painel, cor_material):
        """
        Inicializa um novo orçamento.
        """
        # Validações de campos obrigatórios
        if not cliente:
            raise ValueError("Cliente inválido.")
        if metragem <= 0:
            raise ValueError("Metragem deve ser maior que zero.")
        if valor_estimado <= 0:
            raise ValueError("Valor estimado deve ser maior que zero.")
        if not material.strip():
            raise ValueError("Material é obrigatório.")
        if not t_painel.strip():
            raise ValueError("Tamanho do painel é obrigatório.")
        if cor_material is not None and not cor_material.strip():
            raise ValueError("Cor é obrigatória.")

        # ID único (8 caracteres)
        self.id = str(uuid.uuid4())[:8]

        # Atributos do orçamento
        self.cliente = cliente
        self.metragem = metragem
        self.portao = portao
        self.valor_estimado = valor_estimado
        self.material = material
        self.t_painel = t_painel
        self.cor_material = cor_material

    def __str__(self):
        tem_portao = "Sim" if self.portao else "Não"
        cor_info = f"Cor: {self.cor_material} | " if self.cor_material else ""
        return (
            f"Orçamento ID: {self.id} | "
            f"Cliente: {self.cliente.nome} (ID: {self.cliente.id}) | "
            f"Material: {self.material} | "
            f"Tamanho Painel: {self.t_painel} | "
            f"{cor_info}"
            f"Metragem: {self.metragem}m | "
            f"Portão: {tem_portao} | "
            f"Valor estimado: R$ {self.valor_estimado:.2f}"
        )
