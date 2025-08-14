from cliente import Cliente
from orcamento import Orcamento
from sistema import SistemaOrcamento
from banco_json import carregar_cliente, salvar_cliente
from banco_json import carregar_orcamentos, salvar_orcamento


sistema = SistemaOrcamento()

# --- INICIALIZAÇÃO DO SISTEMA ---
# Carregar clientes salvos no JSON
clientes_salvos = carregar_cliente()
max_id = 0
for c in clientes_salvos:
    # Cadastrar cliente no sistema a partir do JSON
    cliente_cadastrado = sistema.cadastrar_cliente(
        c['nome'], c['telefone'], c['endereco'], c['email'])
    if cliente_cadastrado.id > max_id:
        max_id = cliente_cadastrado.id
# Garante que o próximo ID seja maior que o maior ID carregado
sistema.proximo_id_cliente = max_id + 1

# Carregar orçamentos salvos no JSON
orcamentos_salvos = carregar_orcamentos()
for o in orcamentos_salvos:
    sistema.cadastrar_orcamento(
        o['cliente_id'], o['metragem'], o['portao'], o['valor_estimado'],
        o['material'], o['t_painel'], o['cor_material'])


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
            # Persistência no JSON
            salvar_cliente({
                "id": cliente.id,
                "nome": cliente.nome,
                "telefone": cliente.telefone,
                "endereco": cliente.endereco,
                "email": cliente.email
            })

            print(f"Cliente cadastrado com sucesso: {cliente}")

        except ValueError as e:
            print(f"Erro ao cadastrar cliente: {e}")

    elif opcao == "2":
        buscar_cliente = input(
            "Digite o nome do cliente para cadastrar o orçamento: ").lower()

        while True:
            clientes = sistema.buscar_cliente_por_nome(buscar_cliente)
            if not clientes:
                print(
                    "Cliente não encontrado. Para cadastrar orçamento, o cliente deve existir. Tente novamente.")
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
                "madeira": ["6x6", "6x8"],
                "aluminio": ["4x6", "5x6"],
                "pvc": ["6x6", "6x8"]
            }

            while True:
                material = input(
                    "Qual material (Madeira, Alumínio, PVC): ").strip().lower()
                if material not in materiais:
                    print("Material inválido. Tente novamente.")
                    continue
                break

            opcoes_painel = materiais[material]
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
            if material == "pvc":
                while True:
                    cor_material = input(
                        "Cor do material (Branco, Bege, Marrom, Cinza): ").strip().lower()
                    if cor_material not in ["branco", "bege", "marrom", "cinza"]:
                        print("Cor inválida. Tente novamente.")
                        continue
                    if not cor_material:
                        print("Cor do material não pode ser vazia.")
                        continue
                    break

            metragem = float(
                input("Digite a metragem da cerca (LINEAR FEET): "))
            portao = input("Digite se há portão (sim/não): ").lower() == 'sim'
            valor_estimado = float(input("Digite o valor estimado: "))

            # Cadastra o orçamento no sistema
            orcamento = sistema.cadastrar_orcamento(cliente_id, metragem, portao, valor_estimado,
                                                    material, t_painel, cor_material)

            # Persistência no JSON
            salvar_orcamento({
                "id": orcamento.id, "cliente_id": orcamento.cliente.id,
                "metragem": orcamento.metragem, "portao": orcamento.portao,
                "valor_estimado": orcamento.valor_estimado, "material": orcamento.material,
                "t_painel": orcamento.t_painel, "cor_material": orcamento.cor_material
            })

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
