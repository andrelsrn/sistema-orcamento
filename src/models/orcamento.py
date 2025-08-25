from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..base import Base
import json

class Orcamento(Base):
    __tablename__ = "orcamentos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    metragem = Column(Float, nullable=False)
    portao = Column(Boolean, default=False)
    valor_estimado = Column(Float)
    material = Column(String, nullable=False)
    t_painel = Column(String, nullable=False)
    cor_material = Column(String, nullable=True)
    tamanho_portao = Column(String, nullable=True)
    qnt_portao = Column(Integer, nullable=True)
    # Armazena o dicionário de portões como uma string JSON
    portoes = Column(String, nullable=True)

    cliente = relationship("Cliente", back_populates="orcamentos")

    def __str__(self):
        tem_portao = "Sim" if self.portao else "Não"
        cor_info = f"Cor: {self.cor_material} | " if self.cor_material else ""
        
        # Lida com o caso de portoes ser uma string JSON
        try:
            portoes_dict = json.loads(self.portoes) if self.portoes else {}
        except json.JSONDecodeError:
            portoes_dict = {}

        portoes_info = f"Portões: {portoes_dict} | " if portoes_dict else ""

        return (
            f"Orçamento ID: {self.id} | "
            f"Cliente: {self.cliente.nome} (ID: {self.cliente.id}) | "
            f"Material: {self.material} | "
            f"Tamanho Painel: {self.t_painel} | "
            f"{cor_info}"
            f"Metragem: {self.metragem}m | "
            f"Portão: {tem_portao} | "
            f"Valor estimado: R$ {self.valor_estimado:.2f} | "
            f"{portoes_info}"
        )