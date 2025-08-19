from models.cliente import Cliente
from models.orcamento import Orcamento
from sistema import SistemaOrcamento

sistema = SistemaOrcamento()


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
            cliente = sistema.cadastrar_cliente(
                nome, telefone, endereco, email)

            print(f"Cliente cadastrado com sucesso: {cliente}")

        except ValueError as e:
            print(f"Erro ao cadastrar cliente: {e}")

    elif opcao == "2":
        buscar_cliente = input("Digite o nome do cliente para cadastrar o orçamento: ").lower()

        # Busca o cliente pelo nome
        while True:
            clientes_encontrados = sistema.buscar_cliente_por_nome(buscar_cliente)
            if not clientes_encontrados:
                print("Cliente não encontrado. Tente novamente.")
                buscar_cliente = input("Digite o nome do cliente: ").lower()
            else:
                print("Clientes encontrados:")
                for c in clientes_encontrados:
                    print(c)
                break  # sai do loop ao encontrar clientes

        # Seleciona o ID do cliente
        cliente_ids = [c.id for c in clientes_encontrados]
        cliente_id = int(input("Digite o ID do cliente: "))
        while cliente_id not in cliente_ids:
            print("Id inválido. Tente novamente.")
            cliente_id = int(input("Digite o ID do cliente: "))

        try:
            materiais = {
                "madeira": ["6x6", "6x8"],
                "aluminio": ["4x6", "5x6"],
                "pvc": ["6x6", "6x8"]
            }

            # Escolha do material
            while True:
                material = input("Qual material (Madeira, Alumínio, PVC): ").strip().lower()
                if material not in materiais:
                    print("Material inválido. Tente novamente.")
                    continue
                break

            # Tamanho do painel
            opcoes_painel = materiais[material]
            print("Escolha o tamanho do painel:")
            for i, tamanho in enumerate(opcoes_painel, 1):
                print(f"[{i}] {tamanho}")

            while True:
                escolha = input("Opção: ")
                if escolha in ["1", "2"]:
                    t_painel = opcoes_painel[int(escolha) - 1]
                    break
                print("Opção inválida. Tente novamente.")

            # Cor do PVC
            cor_material = None
            if material == "pvc":
                while True:
                    cor_material = input("Cor do material (Branco, Bege, Marrom, Cinza): ").strip().lower()
                    if cor_material in ["branco", "bege", "marrom", "cinza"]:
                        break
                    print("Cor inválida. Tente novamente.")

            metragem = float(input("Digite a metragem da cerca (LINEAR FEET): "))

            # Portões
            tamanho_portao = qnt_portao = None
            portoes = {}
            portao = input("Digite se há portão (Sim/Não): ").strip().lower()

            if portao == 'sim':
                while True:
                    qnt_portao = input('Quantidade de portão: [Ex: 1 ou 2] ').strip()
                    if qnt_portao.isdigit():
                        qnt_portao = int(qnt_portao)
                        for i in range(qnt_portao):
                            while True:
                                tamanho_portao_input = input(
                                    f'Qual tamanho do portão {i+1} (Single / Double): ').strip().lower()
                                if tamanho_portao_input in ['single', 'double']:
                                    portoes[f'portao_{i+1}'] = tamanho_portao_input
                                    break
                                print("Tamanho inválido. Tente novamente.")
                        break
                    print("Quantidade inválida. Digite um número.")

            # Cadastra o orçamento
            orcamento = sistema.cadastrar_orcamento(
                cliente_id, metragem, portao,
                material, t_painel, cor_material, tamanho_portao, qnt_portao, portoes
            )

            print(f"Orçamento cadastrado com sucesso: {orcamento}")

        except ValueError as e:
            print(f"Erro ao cadastrar orçamento: {e}")

  
    elif opcao == "3":
        orcamentos = sistema.listar_orcamentos()
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
            orcamentos = sistema.consultar_orcamento_por_nome(nome_cliente)
            print(f"Orçamentos encontrados para {nome_cliente}:")
            for orcamento in orcamentos:
                print(orcamento)
        except ValueError as e:
            print(f"Erro ao consultar orçamento: {e}")

    elif opcao == "5":
        print("Saindo do sistema.")
        break
