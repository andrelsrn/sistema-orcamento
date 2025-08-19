from models.cliente import Cliente
from models.orcamento import Orcamento
from db import SessionLocal


def cadastrar_cliente(nome, telefone, endereco, email):
    session = SessionLocal()
    if not nome or not telefone or not endereco or not email:
        raise ValueError("Todos os campos são obrigatórios.")
    try:
        cliente = Cliente(nome, telefone, endereco, email)
        session.add(cliente)
        session.commit()
        session.refresh(cliente)
        return cliente
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
        


def listar_clientes():
    session = SessionLocal()
    try:
        clientes = session.query(Cliente).all()
        return clientes
    finally:
        session.close()


def buscar_cliente_por_nome(nome):
    session = SessionLocal()
    try:
        clientes = session.query(Cliente).filter(
            Cliente.nome.ilike(f"%{nome}%")).all()
        return clientes
    finally:
        session.close()


def atualizar_cliente(cliente_id, nome=None, telefone=None, endereco=None, email=None):
    session = SessionLocal()
    # Atualiza cada campo apenas se um novo valor for fornecido
    try:
        cliente = session.query(Cliente).filter(
            Cliente.id == cliente_id).first()
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

        session.commit()
        session.refresh(cliente)
        return cliente

    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def deletar_cliente(cliente_id):
    session = SessionLocal()

    try:
        cliente = session.query(Cliente).filter(
            Cliente.id == cliente_id).first()
        if not cliente:
            raise ValueError("Cliente não encontrado para exclusão.")

        session.delete(cliente)
        session.commit()
        return True

    except:
        session.rollback()
        raise
    finally:
        session.close()
