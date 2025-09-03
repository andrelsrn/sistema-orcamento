from ..models import Cliente
from sqlalchemy import func
# A importação do SessionLocal não é mais necessária aqui.

def cadastrar_cliente(nome, telefone, endereco, email, db):
    """Cadastra um novo cliente no banco de dados.

    Args:
        nome (str): Nome completo do cliente.
        telefone (str): Telefone de contato.
        endereco (str): Endereço do cliente.
        email (str): E-mail de contato.
        db (Session): A sessão do SQLAlchemy para interagir com o banco.

    Returns:
        Cliente: O objeto Cliente recém-criado.

    Raises:
        ValueError: Se algum dos campos obrigatórios estiver vazio.
    """
    try:
        if not nome or not telefone or not endereco or not email:
            raise ValueError("Todos os campos são obrigatórios.")
        
        cliente = Cliente(nome, telefone, endereco, email)
        db.add(cliente)
        db.commit()
        db.refresh(cliente)
        return cliente
    except Exception as e:
        db.rollback()
        raise e

def listar_clientes(db):
    """Retorna uma lista de todos os clientes."""
    return db.query(Cliente).all()

def buscar_cliente_por_nome(nome, db):
    """Busca clientes cujo nome contenha a string fornecida (case-insensitive)."""
    return db.query(Cliente).filter(func.lower(Cliente.nome).like(f"%{nome.lower()}%")).all()

def atualizar_cliente(cliente_id, db, nome=None, telefone=None, endereco=None, email=None):
    """Atualiza os dados de um cliente existente no banco de dados.

    Apenas os campos fornecidos (diferentes de None) serão atualizados.

    Args:
        cliente_id (int): O ID do cliente a ser atualizado.
        db (Session): A sessão do SQLAlchemy para interagir com o banco.
        nome (str, optional): O novo nome do cliente. Defaults to None.
        telefone (str, optional): O novo telefone do cliente. Defaults to None.
        endereco (str, optional): O novo endereço do cliente. Defaults to None.
        email (str, optional): O novo e-mail do cliente. Defaults to None.

    Returns:
        Cliente: O objeto Cliente com os dados atualizados.

    Raises:
        ValueError: Se o cliente com o ID fornecido não for encontrado.
    """
    try:
        cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
        if not cliente:
            raise ValueError("Cliente não encontrado para atualização.")
        
        if nome is not None:
            cliente.nome = nome
        if telefone is not None:
            cliente.telefone = telefone
        if endereco is not None:
            cliente.endereco = endereco
        if email is not None:
            cliente.email = email

        db.commit()
        db.refresh(cliente)
        return cliente
    except Exception as e:
        db.rollback()
        raise e

def deletar_cliente(cliente_id, db):
    """Deleta um cliente do banco de dados."""
    try:
        cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
        if not cliente:
            raise ValueError("Cliente não encontrado para exclusão.")

        db.delete(cliente)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        raise e