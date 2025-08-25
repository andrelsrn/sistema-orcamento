import re
from .models import Cliente, Orcamento
from .db import SessionLocal

from .services.cliente_service import (
    cadastrar_cliente as service_cadastrar_cliente,
    listar_clientes as service_listar_clientes,
    buscar_cliente_por_nome as service_buscar_cliente_por_nome,
    atualizar_cliente as service_atualizar_cliente,
    deletar_cliente as service_deletar_cliente
)
from .services.orcamento_service import (
    cadastrar_orcamento as service_cadastrar_orcamento,
    listar_orcamentos as service_listar_orcamentos,
    consultar_orcamento_por_nome as service_consultar_orcamento_por_nome
)



def exibir_menu():
    print('-=' * 20)
    print('CADASTRO DE ORCAMENTOS'.center(40))
    print('-=' * 20)

    print("""    [1] - Cadastrar cliente
    [2] - Cadastrar orcamento
    [3] - Listar orcamentos
    [4] - Consultar orcamento por nome
    [5] - Sair""")
    print('-=' * 20)


def orquestrar_cadastro_orcamento(): # Removed 'sistema' parameter
    """Guia o usuário através do processo de criação de um novo orçamento."""
    
    # 1. Encontrar o cliente
    while True:
        buscar_cliente = input("Digite o nome do cliente para o orçamento: ").lower().strip()
        with SessionLocal() as session: # Added session management
            clientes_encontrados = service_buscar_cliente_por_nome(buscar_cliente, db=session) # Updated call
        if clientes_encontrados:
            print("Clientes encontrados:\n") # Added newline for better formatting
            for c in clientes_encontrados:
                print(c)
            break
        print("Nenhum cliente encontrado. Tente novamente.")

    # 2. Selecionar o ID do cliente
    cliente_ids_validos = {str(c.id) for c in clientes_encontrados}
    while True:
        cliente_id_str = input("Digite o ID do cliente selecionado: ").strip()
        if cliente_id_str in cliente_ids_validos:
            cliente_id = int(cliente_id_str)
            break
        print("ID inválido. Por favor, escolha um ID da lista acima.")

    # 3. Detalhes do material
    materiais = {
        "madeira": ["6x6", "6x8"],
        "aluminio": ["4x6", "5x6"],
        "pvc": ["6x6", "6x8"]
    }
    while True:
        material = input("Qual material (Madeira, Alumínio, PVC): ").strip().lower()
        if material in materiais:
            break
        print("Material inválido. Tente novamente.")

    # 4. Tamanho do painel
    opcoes_painel = materiais[material]
    print("Escolha o tamanho do painel:")
    for i, tamanho in enumerate(opcoes_painel, 1):
        print(f"[{i}] {tamanho}")
    while True:
        escolha = input(f"Opção (1-{len(opcoes_painel)}): ").strip()
        if escolha.isdigit() and 1 <= int(escolha) <= len(opcoes_painel):
            t_painel = opcoes_painel[int(escolha) - 1]
            break
        print("Opção inválida.")

    # 5. Cor (apenas para PVC)
    cor_material = None
    if material == "pvc":
        cores_validas = ["branco", "bege", "marrom", "cinza"]
        while True:
            cor_material = input(f"Cor do material ({', '.join(cores_validas)}): ").strip().lower()
            if cor_material in cores_validas:
                break
            print("Cor inválida.")

    # 6. Metragem
    while True:
        try:
            metragem_str = input("Digite a metragem da cerca (em metros): ").strip()
            metragem = float(metragem_str)
            if metragem > 0:
                break
            print("A metragem deve ser um número positivo.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número.")

    # 7. Portões
    portoes = {}
    qnt_portao = 0
    if input("Haverá portão (Sim/Não)? ").strip().lower() == 'sim':
        while True:
            qnt_str = input('Quantidade de portões [Ex: 1 ou 2]: ').strip()
            if qnt_str.isdigit() and int(qnt_str) > 0:
                qnt_portao = int(qnt_str)
                break
            print("Quantidade inválida. Digite um número maior que zero.")
        
        for i in range(qnt_portao):
            while True:
                tamanho_portao = input(f'Qual o tamanho do portão {i+1} (Single / Double): ').strip().lower()
                if tamanho_portao in ['single', 'double']:
                    portoes[f'portao_{i+1}'] = tamanho_portao
                    break
                print("Tamanho inválido. Escolha 'Single' ou 'Double'.")

    # 8. Cadastrar o orçamento através do sistema
    # A função retorna o resultado de service_cadastrar_orcamento
    with SessionLocal() as session: # Added session management
        return service_cadastrar_orcamento( # Updated call
            cliente_id=cliente_id,
            metragem=metragem,
            portao='sim' if qnt_portao > 0 else 'não',
            material=material,
            t_painel=t_painel,
            cor_material=cor_material,
            tamanho_portao=None,
            qnt_portao=qnt_portao,
            portoes=portoes,
            db=session # Passed db=session
        )


while True:
    exibir_menu()
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        # Coleta de dados sem validação duplicada
        nome = input("Digite o nome do cliente: ").strip()
        telefone = input(
            "Digite o telefone do cliente (11 dígitos, com DDD): ").strip()
        endereco = input("Digite o endereco do cliente: ").strip()
        email = input("Digite o email do cliente: ").strip()

        try:
            with SessionLocal() as session: # Added session management
                cliente = service_cadastrar_cliente(
                    nome, telefone, endereco, email, db=session) # Updated call

            print(f"Cliente cadastrado com sucesso: {cliente}")

        except ValueError as e:
            print(f"Erro ao cadastrar cliente: {e}")

    elif opcao == "2":
        try:
            orcamento = orquestrar_cadastro_orcamento() # Removed 'sistema' parameter
            print(f"\nOrçamento cadastrado com sucesso!\n{orcamento}\n")
        except ValueError as e:
            # Erros de validação de dados ou de combinações de materiais
            print(f"\nErro ao cadastrar orçamento: {e}\n")
        except Exception as e:
            # Captura outros erros inesperados para não quebrar o programa
            print(f"\nOcorreu um erro inesperado: {e}\n")

    elif opcao == "3":
        with SessionLocal() as session: # Added session management
            orcamentos = service_listar_orcamentos(db=session) # Updated call
        if not orcamentos:
            print("Nenhum orçamento cadastrado.")
        else:
            print("Orçamentos cadastrados:")
            for orcamento in orcamentos:
                print(orcamento)

    elif opcao == "4":
        nome_cliente = input(
            "Digite o nome do cliente para consultar o orçamento: ")
        try:
            with SessionLocal() as session: # Added session management
                orcamentos = service_consultar_orcamento_por_nome(nome_cliente, db=session) # Updated call
            print(f"Orçamentos encontrados para {nome_cliente}:")
            for orcamento in orcamentos:
                print(orcamento)
        except ValueError as e:
            print(f"Erro ao consultar orçamento: {e}")

    elif opcao == "5":
        print("Saindo do sistema.")
        break
