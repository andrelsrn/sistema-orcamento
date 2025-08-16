import uuid  # Para gerar IDs únicos para os orçamentos


class Orcamento:
    def __init__(self, cliente, metragem, portao, valor_estimado, material, t_painel, cor_material, tamanho_portao, qnt_portao, portoes):
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
        if tamanho_portao is not None and not tamanho_portao.strip():
            raise ValueError("Tamanho do portao é obrigatório.")
        if qnt_portao is not None and qnt_portao <= 0:
            raise ValueError("Quantidade de portao deve ser maior que zero.")



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
        self.tamanho_portao = tamanho_portao
        self.qnt_portao = qnt_portao
        self.portoes = portoes



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
            f"Portão: {tem_portao} | "  #falta implemtar o tamanho portao
            f"Valor estimado: R$ {self.valor_estimado:.2f}"
            f"Tamanho do portao: {self.tamanho_portao}"
            f"Quantidade de portao: {self.qnt_portao}"
            f"Portoes: {self.portoes}"
        )
