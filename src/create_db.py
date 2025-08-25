# Este script cria o banco de dados e as tabelas necessárias.
# Execute este arquivo UMA VEZ antes de rodar o main.py pela primeira vez.

from db import engine
from base import Base

# Importe aqui todos os seus modelos para que eles sejam registrados no metadata do Base
from models import Cliente, Orcamento

print("Iniciando a criação do banco de dados e tabelas...")

# Base.metadata.create_all() inspeciona o engine para ver se a tabela já existe
# antes de criar, então é seguro rodar múltiplas vezes.
Base.metadata.create_all(bind=engine)

print("Banco de dados e tabelas criados com sucesso!")
print("O arquivo 'orcamentos.db' foi criado no diretório do projeto.")
print("Agora você já pode executar o programa principal (main.py).")
