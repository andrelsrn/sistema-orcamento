from ..models import Cliente
from sqlalchemy import func
# A importação do SessionLocal não é mais necessária aqui.

def cadastrar_cliente(nome, telefone, endereco, email, db):
    """Cadastra um novo cliente usando a sessão de banco de dados fornecida."""
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

# CORREÇÃO: Adicionado o argumento 'nome' que estava faltando.
def buscar_cliente_por_nome(nome, db):
    """Busca clientes cujo nome contenha a string fornecida (case-insensitive)."""
    print(f"DEBUG: ClienteService - Nome recebido para busca: '{nome}'")
    print(f"DEBUG: ClienteService - Nome convertido para busca (lower): '{nome.lower()}'")
    
    result = db.query(Cliente).filter(func.lower(Cliente.nome).like(f"%{nome.lower()}%")).all()
    print(f"DEBUG: ClienteService - Resultado da busca (objetos): {result}")
    return result

# CORREÇÃO: Corrigida a indentação e trocado 'session' por 'db'.
def atualizar_cliente(cliente_id, db, nome=None, telefone=None, endereco=None, email=None):
    """Atualiza os dados de um cliente existente."""
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

# CORREÇÃO: Trocado 'session' por 'db'.
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