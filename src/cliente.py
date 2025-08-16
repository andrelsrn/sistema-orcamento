import re


class Cliente:
    """
    Classe que representa um cliente do sistema de orçamentos.
    """

    def __init__(self, nome, id, telefone, endereco, email):
        """
        Inicializa um novo cliente.

        Parâmetros:
            nome (str): Nome do cliente.
            id (int): ID único do cliente.
            telefone (str): Telefone do cliente (com DDD, 11 dígitos).
            endereco (str): Endereço do cliente.
            email (str): Email do cliente.

        Levanta ValueError se algum dado for inválido.
        """
        nome = nome.strip()
        telefone = telefone.strip()
        endereco = endereco.strip()
        email = email.strip()

        if not nome or not nome.replace(" ", "").isalpha():
            raise ValueError("Nome inválido. Deve conter apenas letras.")

        # Validação do telefone: exatamente 11 dígitos numéricos
        if not re.match(r"^\d{11}$", telefone):
            raise ValueError(
                "Telefone deve conter exatamente 11 números (com DDD).")

        if not endereco:
            raise ValueError("Endereço não pode ser vazio.")

        # Validação simples do email (exige formato básico com '@' e domínio)
        if not re.fullmatch(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            raise ValueError("Formato de Email inválido.")

        self.id = id
        self.nome = nome
        self.telefone = telefone
        self.endereco = endereco
        self.email = email

        # Lista para armazenar os orçamentos associados a este cliente
        self.orcamentos = []

    def __str__(self):
        return (
            f"ID: {self.id} | Nome: {self.nome} | Telefone: {self.telefone} | "
            f"Endereço: {self.endereco} | Email: {self.email}"
        )
