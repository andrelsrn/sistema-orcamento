import uuid  # Para gerar IDs únicos para os orçamentos


class Orcamento:
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

    def __init__(self, cliente, metragem, portao, valor_estimado, material, t_painel, cor_material, tamanho_portao, qnt_portao, portoes):
        """
        Inicializa um novo orçamento.
        """
        # Validações de campos obrigatórios
        if not cliente:
            raise ValueError("Cliente inválido.")
        if metragem <= 0:
            raise ValueError("Metragem deve ser maior que zero.")
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
        self.calcular_orcamento()

    def calcular_orcamento(self):
        # Monta a chave: inclui a cor apenas se for PVC
        valor_base = (self.material, self.t_painel, self.cor_material) if self.material == 'pvc' else (
            self.material, self.t_painel)

        if valor_base in self.tabela_precos:
            preco_metro = self.tabela_precos[valor_base]
            valor_total = preco_metro * self.metragem
            if self.portao:
                valor_total += self.valor_portao * self.qnt_portao
            self.valor_estimado = valor_total
            return self.valor_estimado
        else:
            return None

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
            f"Portão: {tem_portao} | "  # falta implemtar o tamanho portao
            f"Valor estimado: R$ {self.valor_estimado:.2f} | "
            f"Tamanho do portao: {self.tamanho_portao} | "
            f"Quantidade de portao: {self.qnt_portao} | "
            f"Portoes: {self.portoes} | "
        )
