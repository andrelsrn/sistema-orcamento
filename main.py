from cliente import Cliente
from orcamento import Orcamento
from sistema import SistemaOrcamento

sistema = SistemaOrcamento()


def exibir_menu():
    print("""    [1] - Cadastrar cliente,
    [2] - Cadastrar orcamento,
    [3] - Listar orcamentos,
    [4] - Consultar orcamento por nome,
    [5] - Sair""")


while True:
    exibir_menu()
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        while True:
            nome = input("Digite o nome do cliente: ").strip()
            if not nome.replace(" ", "").isalpha():
                print("Nome inválido. Deve conter apenas letras. Tente novamente.")
            else:
                break
        while True:
            telefone = input("Digite o telefone do cliente: ")
            if not telefone.isdigit() or len(telefone) < 11:
                print(
                    "Telefone inválido. Deve conter apenas números e ter 11 dígitos. Tente novamente.")
            else:
                break
        while True:
            endereco = input("Digite o endereco do cliente: ")
            if not endereco.strip():
                print("Endereço não pode ser vazio. Tente novamente.")
            else:
                break
        while True:
            email = input("Digite o email do cliente: ").strip()
            if "@" not in email or "." not in email:
                print("Formato de Email inválido. Tente novamente.")
            else:
                break
        try:
            cliente = sistema.cadastrar_cliente(
                nome, telefone, endereco, email)
            print(f"Cliente cadastrado com sucesso: {cliente}")
        except ValueError as e:
            print(f"Erro ao cadastrar cliente: {e}")

    elif opcao == "2":
        buscar_cliente = input("Digite o nome do cliente para cadastrar o orçamento: ").lower()

        while True:
            clientes = sistema.buscar_cliente_por_nome(buscar_cliente)
            if not clientes:
                print("Cliente não encontrado. Para cadastrar orçamento, o cliente deve existir. Tente novamente.")
                buscar_cliente = input("Digite o nome do cliente: ").lower()
            else:
                print("Clientes encontrados:")
                for cliente in clientes:
                    print(cliente)
                break

        try:
            cliente_id = int(input("Digite o ID do cliente: "))
            while cliente_id not in [c.id for c in sistema.clientes]:
                print("Id inválido. Tente novamente.")
                cliente_id = int(input("Digite o ID do cliente: "))

            materiais = {
                "Madeira": ["6x6", "6x8"],
                "Alumínio": ["4x6", "5x6"],
                "PVC": ["6x6", "6x8"]
            }

            while True:
                tipo_de_cerca = input("Qual material (Madeira, Alumínio, PVC): ").title()
                if tipo_de_cerca not in materiais:
                    print("Material inválido. Tente novamente.")
                    continue
                break

            opcoes_painel = materiais[tipo_de_cerca]
            print("Escolha o tamanho do painel:")
            for i, tamanho in enumerate(opcoes_painel, 1):
                print(f"[{i}] {tamanho}")

            while True:
                escolha = input("Opção: ")
                if escolha not in ["1", "2"]:
                    print("Opção inválida. Tente novamente.")
                    continue
                t_painel = opcoes_painel[int(escolha) - 1]
                break

            cor_material = None
            if tipo_de_cerca == "PVC":
                while True:
                    cor_material = input("Cor do material (Branco, Preto, Cinza): ").title()
                    if not cor_material:
                        print("Cor do material não pode ser vazia.")
                        continue
                    break
            else:
                cor_material = ""  # Para materiais que não sejam PVC, pode deixar vazio

            metragem = float(input("Digite a metragem da cerca (LINEAR FEET): "))
            portao = input("Digite se há portão (sim/não): ").lower() == 'sim'
            valor_estimado = float(input("Digite o valor estimado: "))

            orcamento = sistema.cadastrar_orcamento(
                cliente_id, tipo_de_cerca, metragem, portao, valor_estimado, tipo_de_cerca, t_painel, cor_material
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
