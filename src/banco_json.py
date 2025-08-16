import json  # Importa o módulo para trabalhar com arquivos JSON
from pathlib import Path

# --- CONFIGURAÇÃO DE CAMINHOS ---
# Path(__file__) é o caminho para este arquivo (banco_json.py)
# .resolve().parent vai para o diretório que contém o arquivo (src/)
# .parent novamente vai para o diretório pai (a raiz do projeto)
# A partir da raiz, construímos o caminho para o diretório 'data'
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data'

# Garante que o diretório 'data' exista. Se não, ele será criado.
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Caminhos completos para os arquivos JSON
CLIENTES_FILE = DATA_DIR / 'clientes.json'
ORCAMENTOS_FILE = DATA_DIR / 'orcamentos.json'


def carregar_cliente():
    """
    Lê os clientes do arquivo 'clientes.json' e retorna como uma lista de dicionários.
    Se o arquivo não existir, retorna uma lista vazia.
    """
    try:
        # Abre o arquivo no modo leitura ('r') com codificação UTF-8 e carrega o conteúdo JSON
        with open(CLIENTES_FILE, 'r', encoding='utf-8') as arquivo:
            clientes = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        # Se o arquivo não existir ou estiver vazio/corrompido, inicializa uma lista vazia
        clientes = []
    return clientes  # Retorna a lista de clientes


def salvar_cliente(novo_cliente):
    """
    Recebe um dicionário representando um novo cliente, adiciona à lista de clientes
    existente e salva novamente no arquivo 'clientes.json'.
    """
    clientes = carregar_cliente()  # Carrega a lista atual de clientes
    clientes.append(novo_cliente)  # Adiciona o novo cliente à lista

    # Abre o arquivo no modo escrita ('w') e salva a lista atualizada
    with open(CLIENTES_FILE, 'w', encoding='utf-8') as arquivo:
        # json.dump escreve a lista em formato JSON, indent=4 deixa legível
        json.dump(clientes, arquivo, indent=4, ensure_ascii=False)


def salvar_todos_clientes(lista_de_clientes):
    """
    Recebe uma lista completa de objetos Cliente, converte para dicionários
    e sobrescreve o arquivo 'clientes.json' com os dados atualizados.
    """
    # Converte a lista de objetos Cliente para uma lista de dicionários
    # de forma explícita para evitar salvar dados indesejados (como a lista de orçamentos).
    clientes_dict = [
        {
            "id": c.id,
            "nome": c.nome,
            "telefone": c.telefone,
            "endereco": c.endereco,
            "email": c.email
        }
        for c in lista_de_clientes]
    with open(CLIENTES_FILE, 'w', encoding='utf-8') as arquivo:
        # Salva a lista inteira, sobrescrevendo o conteúdo anterior
        json.dump(clientes_dict, arquivo, indent=4, ensure_ascii=False)


def carregar_orcamentos():
    """
    Lê os orçamentos do arquivo 'orcamentos.json' e retorna como lista de dicionários.
    Se o arquivo não existir, retorna uma lista vazia.
    """
    try:
        with open(ORCAMENTOS_FILE, 'r', encoding='utf-8') as arquivo:
            orcamentos = json.load(arquivo)  # Converte JSON em lista Python
    except (FileNotFoundError, json.JSONDecodeError):
        orcamentos = []  # Se não existir ou estiver vazio/corrompido, retorna lista vazia
    return orcamentos


def salvar_orcamento(novo_orcamento):
    """
    Recebe um dicionário representando um novo orçamento, adiciona à lista
    existente e salva novamente no arquivo 'orcamentos.json'.
    """
    orcamentos = carregar_orcamentos()  # Carrega lista existente
    orcamentos.append(novo_orcamento)   # Adiciona o novo orçamento

    with open(ORCAMENTOS_FILE, 'w', encoding='utf-8') as arquivo:
        # Salva lista atualizada no JSON
        json.dump(orcamentos, arquivo, indent=4, ensure_ascii=False)
