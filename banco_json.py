import json  # Importa o módulo para trabalhar com arquivos JSON


def carregar_cliente():
    """
    Lê os clientes do arquivo 'clientes.json' e retorna como uma lista de dicionários.
    Se o arquivo não existir, retorna uma lista vazia.
    """
    try:
        # Abre o arquivo no modo leitura ('r') e carrega o conteúdo JSON
        with open('clientes.json', 'r') as arquivo:
            # Converte o JSON em lista de dicionários
            clientes = json.load(arquivo)
    except FileNotFoundError:
        # Se o arquivo não existir, inicializa uma lista vazia
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
    with open('clientes.json', 'w') as arquivo:
        # json.dump escreve a lista em formato JSON, indent=4 deixa legível
        json.dump(clientes, arquivo, indent=4)


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
    with open('clientes.json', 'w') as arquivo:
        # Salva a lista inteira, sobrescrevendo o conteúdo anterior
        json.dump(clientes_dict, arquivo, indent=4)


def carregar_orcamentos():
    """
    Lê os orçamentos do arquivo 'orcamentos.json' e retorna como lista de dicionários.
    Se o arquivo não existir, retorna uma lista vazia.
    """
    try:
        with open('orcamentos.json', 'r') as arquivo:
            orcamentos = json.load(arquivo)  # Converte JSON em lista Python
    except FileNotFoundError:
        orcamentos = []  # Se não existir, retorna lista vazia
    return orcamentos


def salvar_orcamento(novo_orcamento):
    """
    Recebe um dicionário representando um novo orçamento, adiciona à lista
    existente e salva novamente no arquivo 'orcamentos.json'.
    """
    orcamentos = carregar_orcamentos()  # Carrega lista existente
    orcamentos.append(novo_orcamento)   # Adiciona o novo orçamento

    with open('orcamentos.json', 'w') as arquivo:
        # Salva lista atualizada no JSON
        json.dump(orcamentos, arquivo, indent=4)
