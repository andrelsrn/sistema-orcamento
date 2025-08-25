from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..base import Base  # <--- importa a Base
import re  # Importa o módulo de expressões regulares para validação

class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    endereco = Column(String, nullable=False)
    email = Column(String, nullable=False)
    orcamentos = relationship("Orcamento", back_populates="cliente")

    def __init__(self, nome, telefone, endereco, email):
        """
        Inicializa um novo cliente.

        Parâmetros:
            nome (str): Nome do cliente.
            telefone (str): Telefone do cliente (com DDD, 11 dígitos).
            endereco (str): Endereço do cliente.
            email (str): Email do cliente.

        Levanta ValueError se algum dado for inválido.
        """
        nome = nome.strip()
        telefone = telefone.strip()
        endereco = endereco.strip()
        email = email.strip()

        if not nome.strip():
            raise ValueError("Nome não pode ser vazio ou conter apenas espaços.")

        # Validação do telefone: exatamente 11 dígitos numéricos
        if not re.match(r"^\d{11}$", telefone):
            raise ValueError(
                "Telefone deve conter exatamente 11 números (com DDD).")

        if not endereco:
            raise ValueError("Endereço não pode ser vazio.")

        # Validação simples do email (exige formato básico com '@' e domínio)
        if not re.fullmatch(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            raise ValueError("Formato de Email inválido.")

        self.nome = nome
        self.telefone = telefone
        self.endereco = endereco
        self.email = email

    def __str__(self):
        return (
            f"ID: {self.id} | Nome: {self.nome} | Telefone: {self.telefone} | "
            f"Endereço: {self.endereco} | Email: {self.email}"
        )
