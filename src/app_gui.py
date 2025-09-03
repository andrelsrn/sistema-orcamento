import customtkinter as ctk
from tkinter import ttk
from .db import SessionLocal
from .services.cliente_service import buscar_cliente_por_nome, listar_clientes, cadastrar_cliente
from .gerador_pdf import gerar_orcamento
from .services.orcamento_service import cadastrar_orcamento, listar_orcamentos
from .models import Cliente, Orcamento
import re
import os
import threading
import queue
from sqlalchemy.orm import joinedload
import traceback
from .services.email_service import enviar_email_smtp
from .gerador_pdf import criar_corpo_html_orcamento


class App(ctk.CTk):
    def __init__(self):
        """Inicializa a aplicação principal da GUI e configura todos os widgets."""
        super().__init__()

        self.title("Sistema de Orçamentos de Cerca")
        self.geometry("800x650")

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.materiais_data = {
            "Madeira": ["6x6", "6x8"],
            "Alumínio": ["4x6", "5x6"],
            "PVC": ["6x6", "6x8"]
        }

        self.gate_widgets = []
        self.found_clients = []
        self.selected_client_id = None

        self.tab_view = ctk.CTkTabview(self, width=780)
        self.tab_view.pack(padx=10, pady=10, fill="both", expand=True)

        self.tab_view.add("Cadastrar Orçamento")
        self.tab_view.add("Consultar Orçamentos")
        self.tab_view.add("Clientes")
        self.tab_view.add("Cadastrar Cliente")

        # --- Aba: Cadastrar Orçamento ---
        self.tab_1_frame = self.tab_view.tab("Cadastrar Orçamento")
        self.tab_1_frame.grid_columnconfigure(1, weight=1)

        # -- Cliente --
        self.client_label = ctk.CTkLabel(
            self.tab_1_frame, text="Buscar Cliente:")
        self.client_label.grid(row=0, column=0, padx=20,
                               pady=(20, 10), sticky="w")
        self.client_entry = ctk.CTkEntry(
            self.tab_1_frame, placeholder_text="Digite o nome do cliente para buscar")
        self.client_entry.grid(row=0, column=1, padx=(
            0, 10), pady=(20, 10), sticky="ew")

        self.client_search_button = ctk.CTkButton(
            self.tab_1_frame, text="Buscar", width=80, command=self.buscar_e_selecionar_cliente)
        self.client_search_button.grid(row=0, column=2, padx=10, pady=(20, 10))

        self.client_selection_combobox = ctk.CTkComboBox(self.tab_1_frame, values=[
                                                         "Nenhum cliente encontrado"], command=self.on_client_select)
        self.client_selection_combobox.grid(
            row=1, column=1, columnspan=2, padx=(0, 10), pady=(0, 10), sticky="ew")
        self.client_selection_combobox.set("Nenhum cliente encontrado")
        self.client_selection_combobox.configure(state="disabled")

        self.client_status_label = ctk.CTkLabel(
            self.tab_1_frame, text="", text_color="green")
        self.client_status_label.grid(
            row=2, column=0, columnspan=3, padx=20, pady=(0, 10), sticky="ew")

        # -- Material --
        self.material_label = ctk.CTkLabel(self.tab_1_frame, text="Material:")
        self.material_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        self.material_combobox = ctk.CTkComboBox(self.tab_1_frame, values=list(
            self.materiais_data.keys()), command=self.update_panel_options)
        self.material_combobox.grid(
            row=3, column=1, columnspan=2, padx=(0, 10), pady=10, sticky="ew")

        # -- Tamanho do Painel --
        self.panel_label = ctk.CTkLabel(
            self.tab_1_frame, text="Tamanho do Painel:")
        self.panel_label.grid(row=4, column=0, padx=20, pady=10, sticky="w")
        self.panel_combobox = ctk.CTkComboBox(self.tab_1_frame, values=[])
        self.panel_combobox.grid(
            row=4, column=1, columnspan=2, padx=(0, 10), pady=10, sticky="ew")

        # -- Cor --
        self.color_label = ctk.CTkLabel(
            self.tab_1_frame, text="Cor do Material (PVC):")
        self.color_label.grid(row=5, column=0, padx=20, pady=10, sticky="w")
        self.color_combobox = ctk.CTkComboBox(
            self.tab_1_frame, values=["Branco", "Bege", "Marrom", "Cinza"])
        self.color_combobox.grid(
            row=5, column=1, columnspan=2, padx=(0, 10), pady=10, sticky="ew")

        # -- Metragem --
        self.footage_label = ctk.CTkLabel(
            self.tab_1_frame, text="Metragem (metros):")
        self.footage_label.grid(row=6, column=0, padx=20, pady=10, sticky="w")
        self.footage_entry = ctk.CTkEntry(
            self.tab_1_frame, placeholder_text="Ex: 50.5")
        self.footage_entry.grid(
            row=6, column=1, columnspan=2, padx=(0, 10), pady=10, sticky="ew")

        # -- Portão --
        self.gate_check = ctk.CTkCheckBox(
            self.tab_1_frame, text="Adicionar Portão?", command=self.toggle_gate_fields)
        self.gate_check.grid(row=7, column=0, padx=20, pady=10, sticky="w")

        # Widgets do portão
        self.gate_qty_label = ctk.CTkLabel(
            self.tab_1_frame, text="Quantidade de Portões:")
        self.gate_qty_entry = ctk.CTkEntry(
            self.tab_1_frame, placeholder_text="Ex: 1")
        self.gate_qty_entry.bind("<KeyRelease>", self.update_gate_fields)

        self.gate_sizes_frame = ctk.CTkScrollableFrame(
            self.tab_1_frame, label_text="Tamanhos dos Portões")

        # -- Botão de Cadastro --
        self.submit_button = ctk.CTkButton(
            self.tab_1_frame, text="Cadastrar Orçamento", command=self.submit_form)
        self.submit_button.grid(
            row=10, column=0, columnspan=3, padx=20, pady=20, sticky="ew")

        # --- Aba: Consultar Orçamentos ---
        self.tab_2_frame = self.tab_view.tab("Consultar Orçamentos")

        # Frame para scroll de orçamentos
        self.scrollable_frame = ctk.CTkScrollableFrame(self.tab_2_frame)
        self.scrollable_frame.pack(expand=True, fill="both", padx=10, pady=10)
        columns = ("ID", "Cliente", "Metragem", "Portão", "Qty Portão",
                   "Material", "Tamanho Painel", "Cor Material", "Valor Estimado")
        self.tree = ttk.Treeview(
            self.scrollable_frame, columns=columns, show="headings", height=10)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")

        self.tree.pack(expand=True, fill="both")

        # Adiciona o "ouvinte" para seleção na lista
        self.tree.bind("<<TreeviewSelect>>", self.on_orcamento_select)

        # Frame para o botão
        self.tab_2_button_frame = ctk.CTkFrame(
            self.tab_2_frame, fg_color="transparent")
        self.tab_2_button_frame.pack(pady=10, fill="x", padx=10)

        # Botão para atualizar a lista
        self.btn_atualizar = ctk.CTkButton(
            self.tab_2_button_frame, text="Atualizar Orçamentos", command=self.carregar_orcamentos)
        self.btn_atualizar.pack(side="left", expand=True, padx=(0, 5))

        # Botão para enviar e-mail, começando desabilitado
        self.btn_enviar_email = ctk.CTkButton(self.tab_2_button_frame, text="Enviar Orçamento por E-mail",
                                              command=self.enviar_orcamento_email, state="disabled")
        self.btn_enviar_email.pack(side="left", expand=True, padx=(5, 0))

        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(
            self.scrollable_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Aba: Clientes
        self.tab_3_frame = self.tab_view.tab("Clientes")

        self.client_scrollable_frame = ctk.CTkScrollableFrame(self.tab_3_frame)
        self.client_scrollable_frame.pack(
            expand=True, fill="both", padx=10, pady=10)
        client_columns = ("ID", "Nome", "Email", "Telefone")
        self.client_tree = ttk.Treeview(
            self.client_scrollable_frame, columns=client_columns, show="headings", height=10)
        for col in client_columns:
            self.client_tree.heading(col, text=col)
            self.client_tree.column(col, width=150, anchor="center")
        self.client_tree.pack(expand=True, fill="both")
        client_scrollbar = ttk.Scrollbar(
            self.client_scrollable_frame, orient="vertical", command=self.client_tree.yview)
        self.client_tree.configure(yscroll=client_scrollbar.set)
        client_scrollbar.pack(side="right", fill="y")
        btn_atualizar_clientes = ctk.CTkButton(
            self.tab_3_frame, text="Atualizar Clientes", command=self.carregar_clientes)
        btn_atualizar_clientes.pack(pady=5)

        # --- Aba: Cadastrar Cliente ---
        self.tab_4_frame = self.tab_view.tab("Cadastrar Cliente")
        self.tab_4_frame.grid_columnconfigure(1, weight=1)

        # Campos para cadastrar cliente
        lbl_nome = ctk.CTkLabel(self.tab_4_frame, text="Nome:")
        lbl_nome.grid(row=0, column=0, padx=20, pady=(20, 8), sticky="w")
        self.entry_nome_cliente = ctk.CTkEntry(
            self.tab_4_frame, placeholder_text="Nome completo")
        self.entry_nome_cliente.grid(
            row=0, column=1, padx=(0, 10), pady=(20, 8), sticky="ew")

        lbl_email = ctk.CTkLabel(self.tab_4_frame, text="Email:")
        lbl_email.grid(row=1, column=0, padx=20, pady=8, sticky="w")
        self.entry_email_cliente = ctk.CTkEntry(
            self.tab_4_frame, placeholder_text="exemplo@dominio.com")
        self.entry_email_cliente.grid(
            row=1, column=1, padx=(0, 10), pady=8, sticky="ew")

        lbl_telefone = ctk.CTkLabel(self.tab_4_frame, text="Telefone:")
        lbl_telefone.grid(row=2, column=0, padx=20, pady=8, sticky="w")
        self.entry_telefone_cliente = ctk.CTkEntry(
            self.tab_4_frame, placeholder_text="Apenas números")
        self.entry_telefone_cliente.grid(
            row=2, column=1, padx=(0, 10), pady=8, sticky="ew")

        lbl_endereco = ctk.CTkLabel(self.tab_4_frame, text="Endereço:")
        lbl_endereco.grid(row=3, column=0, padx=20, pady=8, sticky="w")
        self.entry_endereco_cliente = ctk.CTkEntry(
            self.tab_4_frame, placeholder_text="Rua, Nº, Bairro")
        self.entry_endereco_cliente.grid(
            row=3, column=1, padx=(0, 10), pady=8, sticky="ew")

        self.btn_cadastrar_cliente = ctk.CTkButton(
            self.tab_4_frame, text="Cadastrar Cliente", command=self.submit_cliente)
        self.btn_cadastrar_cliente.grid(
            row=4, column=0, columnspan=2, padx=20, pady=15, sticky="ew")

        self.client_create_status_label = ctk.CTkLabel(
            self.tab_4_frame, text="", text_color="green")
        self.client_create_status_label.grid(
            row=5, column=0, columnspan=2, padx=20, pady=(0, 10), sticky="ew")

        # --- Inicialização ---
        self.update_panel_options(self.material_combobox.get())
        self.toggle_gate_fields()

    def buscar_e_selecionar_cliente(self):
        """Busca clientes pelo nome e atualiza o combobox de seleção."""
        nome_cliente = self.client_entry.get().strip()
        if not nome_cliente:
            self.client_status_label.configure(
                text="Digite um nome para buscar.", text_color="orange")
            return

        with SessionLocal() as session:
            self.found_clients = buscar_cliente_por_nome(nome_cliente, session)

        if self.found_clients:
            # Formata a lista para exibição: "Nome (ID: 1)"
            display_values = [
                f"{c.nome} (ID: {c.id})" for c in self.found_clients]
            self.client_selection_combobox.configure(
                values=display_values, state="normal")
            # Seleciona o primeiro por padrão
            self.client_selection_combobox.set(display_values[0])
            # Chama a função para atualizar o ID
            self.on_client_select(display_values[0])
            self.client_status_label.configure(
                text=f"{len(self.found_clients)} cliente(s) encontrado(s).", text_color="green")
        else:
            self.client_selection_combobox.configure(
                values=["Nenhum cliente encontrado"], state="disabled")
            self.client_selection_combobox.set("Nenhum cliente encontrado")
            self.selected_client_id = None
            self.client_status_label.configure(
                text="Nenhum cliente encontrado com esse nome.", text_color="orange")

    def on_client_select(self, selected_display_value: str):
        """Atualiza o ID do cliente selecionado com base no valor do combobox."""
        match = re.search(r"\(ID: (\d+)\)", selected_display_value)
        if match:
            self.selected_client_id = int(match.group(1))
        else:
            self.selected_client_id = None

    def update_panel_options(self, material: str):
        """Atualiza as opções de painel E o estado do campo de cor."""
        # Atualiza tamanhos do painel
        panel_sizes = self.materiais_data.get(material, [])
        self.panel_combobox.configure(values=panel_sizes)
        if panel_sizes:
            self.panel_combobox.set(panel_sizes[0])
        else:
            self.panel_combobox.set("")

        # Habilita/Desabilita campo de cor
        if material == "PVC":
            self.color_combobox.configure(state="normal")
            self.color_label.configure(
                text_color="white") # Indica que está habilitado
        else:
            self.color_combobox.configure(state="disabled")
            # Indica que está desabilitado
            self.color_label.configure(text_color="gray")

    def toggle_gate_fields(self):
        """Mostra ou esconde os campos de quantidade e o frame dos tamanhos."""
        if self.gate_check.get() == 1:
            self.gate_qty_label.grid(
                row=8, column=0, padx=20, pady=10, sticky="w")
            self.gate_qty_entry.grid(
                row=8, column=1, columnspan=2, padx=(0, 10), pady=10, sticky="ew")
            self.gate_sizes_frame.grid(
                row=9, column=0, columnspan=3, padx=20, pady=10, sticky="nsew")
            self.update_gate_fields()
        else:
            self.gate_qty_label.grid_forget()
            self.gate_qty_entry.grid_forget()
            self.gate_sizes_frame.grid_forget()
            # Limpa os campos quando desmarcado
            self.gate_qty_entry.delete(0, ctk.END)
            self.update_gate_fields()

    def update_gate_fields(self, event=None):
        """Cria campos de tamanho de portão dinamicamente com base na quantidade."""
        for widget in self.gate_widgets:
            widget.destroy()
        self.gate_widgets.clear()

        try:
            qty_str = self.gate_qty_entry.get()
            qty = int(qty_str) if qty_str else 0
        except ValueError:
            qty = 0

        if qty > 10:
            qty = 10
            # Impõe um limite de 10 na quantidade de portões para evitar excesso de widgets.
            self.gate_qty_entry.delete(0, ctk.END)
            self.gate_qty_entry.insert(0, str(qty))
            self.client_status_label.configure(
                text="Máximo de 10 portões para visualização.", text_color="orange")

        for i in range(qty):
            gate_size_label = ctk.CTkLabel(
                self.gate_sizes_frame, text=f"Tamanho do Portão {i+1}:")
            gate_size_label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
            self.gate_widgets.append(gate_size_label)

            gate_size_combobox = ctk.CTkComboBox(
                self.gate_sizes_frame, values=["Single", "Double"])
            gate_size_combobox.set("Single")  # Valor padrão
            gate_size_combobox.grid(
                row=i, column=1, padx=10, pady=5, sticky="ew")
            self.gate_widgets.append(gate_size_combobox)

    def submit_form(self):
        """Coleta os dados do formulário, valida e tenta cadastrar o orçamento."""
        self.client_status_label.configure(text="")  # Limpa mensagens

        # 1. Validação do Cliente
        if self.selected_client_id is None:
            self.client_status_label.configure(
                text="Erro: Cliente não selecionado. Busque e selecione um cliente.", text_color="red")
            return

        # 2. Coleta e Validação de Dados
        material = self.material_combobox.get()
        t_painel = self.panel_combobox.get()
        cor_material = self.color_combobox.get() if material == "PVC" else None
        metragem_str = self.footage_entry.get().strip()

        # Validações...
        if not material or not t_painel:
            self.client_status_label.configure(
                text="Erro: Material e Tamanho do Painel são obrigatórios.", text_color="red")
            return
        if material == "PVC" and not cor_material:
            self.client_status_label.configure(
                text="Erro: Cor é obrigatória para material PVC.", text_color="red")
            return
        try:
            metragem = float(metragem_str.replace(',', '.'))
            if metragem <= 0:
                raise ValueError
        except (ValueError, TypeError):
            self.client_status_label.configure(
                text="Erro: Metragem inválida. Use um número positivo.", text_color="red")
            return

        # 3. Dados do Portão
        # (Seu código de dados do portão está bom, sem alterações necessárias)
        tem_portao = self.gate_check.get() == 1
        qnt_portao = 0
        portoes_data = {}
        if tem_portao:
            try:
                qnt_portao_str = self.gate_qty_entry.get()
                qnt_portao = int(qnt_portao_str) if qnt_portao_str else 0
                if qnt_portao <= 0:
                    raise ValueError
            except (ValueError, TypeError):
                self.client_status_label.configure(
                    text="Erro: Quantidade de portões inválida.", text_color="red")
                return

            gate_comboboxes = [
                w for w in self.gate_widgets if isinstance(w, ctk.CTkComboBox)]
            if len(gate_comboboxes) != qnt_portao:
                self.client_status_label.configure(
                    text="Erro: Pressione Enter no campo de quantidade de portões para atualizar.", text_color="red")
                return

            for i, cb in enumerate(gate_comboboxes):
                size = cb.get()
                if not size:
                    self.client_status_label.configure(
                        text=f"Erro: Tamanho do portão {i+1} é obrigatório.", text_color="red")
                    return
                portoes_data[f'portao_{i+1}'] = size

        # 4. Chamada ao Serviço
        try:
            with SessionLocal() as session:
                orcamento_cadastrado = cadastrar_orcamento(
                    cliente_id=self.selected_client_id,  # Usando o ID selecionado
                    metragem=metragem,
                    portao='sim' if tem_portao else 'não',
                    material=material,
                    t_painel=t_painel,
                    cor_material=cor_material,
                    tamanho_portao=None,
                    qnt_portao=qnt_portao,
                    portoes=portoes_data,
                    db=session
                )
            self.client_status_label.configure(
                text=f"Orçamento cadastrado com sucesso! ID: {orcamento_cadastrado.id}", text_color="green")
            self.clear_form()

        except ValueError as ve:
            self.client_status_label.configure(
                text=f"Erro de validação: {ve}", text_color="red")
        except Exception as e:
            self.client_status_label.configure(
                text=f"Erro ao cadastrar: {e}", text_color="red")

    def clear_form(self):
        """Limpa os campos do formulário após o cadastro."""
        self.client_entry.delete(0, ctk.END)
        self.material_combobox.set(list(self.materiais_data.keys())[0])
        self.update_panel_options(self.material_combobox.get())
        self.color_combobox.set("Branco")
        self.footage_entry.delete(0, ctk.END)
        self.gate_check.deselect()
        self.toggle_gate_fields()
        self.client_selection_combobox.configure(
            values=["Nenhum cliente encontrado"], state="disabled")
        self.client_selection_combobox.set("Nenhum cliente encontrado")
        self.found_clients = []
        self.selected_client_id = None
        # Agenda a limpeza da mensagem de status para 5 segundos no futuro.
        self.after(5000, lambda: self.client_status_label.configure(text=""))

    def carregar_orcamentos(self):
        """Busca os orçamentos no banco de dados e atualiza a tabela na GUI."""
        with SessionLocal() as session:
            orcamentos = listar_orcamentos(session)
            for i in self.tree.get_children():
                self.tree.delete(i)
            for o in orcamentos:
                self.tree.insert("", "end", values=(
                    o.id, o.cliente.nome, o.metragem, o.portao, o.qnt_portao,
                    o.material, o.t_painel, o.cor_material or "-", o.valor_estimado
                ))

    def carregar_clientes(self):
        """Busca os clientes no banco de dados e atualiza a tabela na GUI."""
        with SessionLocal() as session:
            clientes = listar_clientes(session)
            for i in self.client_tree.get_children():
                self.client_tree.delete(i)
            for c in clientes:
                self.client_tree.insert("", "end", values=(
                    c.id, c.nome, c.email, c.telefone))

    def on_orcamento_select(self, event=None):
        """Ativa o botão de e-mail se um item estiver selecionado."""
        if self.tree.selection():
            self.btn_enviar_email.configure(state="normal")
        else:
            self.btn_enviar_email.configure(state="disabled")

    def enviar_orcamento_email(self):
        """
        Inicia o processo de envio de e-mail em uma thread separada
        para manter a interface responsiva.
        """
        selected_item = self.tree.selection()
        if not selected_item:
            return

        orcamento_id = self.tree.item(selected_item, "values")[0]

        # Fila para receber o resultado (sucesso ou erro) da thread de trabalho.
        self.resultado_fila = queue.Queue()

        # Define e inicia a thread para executar a tarefa pesada.
        worker_thread = threading.Thread(
            target=self.tarefa_de_envio,
            args=(int(orcamento_id), self.resultado_fila)
        )
        # Permite que o app feche mesmo se a thread estiver rodando.
        worker_thread.daemon = True
        worker_thread.start()

        # Exibe uma mensagem de status inicial para o usuário.
        self.status_label = ctk.CTkLabel(
            self.tab_2_frame, text=f"Processando orçamento {orcamento_id}...", text_color="yellow")
        self.status_label.pack(pady=5)

        # Inicia o método que verifica a fila de resultados periodicamente.
        self.verificar_fila_de_resultados()

    def tarefa_de_envio(self, orcamento_id, fila):
        """
        Executa a geração de PDF e o envio de e-mail em segundo plano.
        """

        caminho_pdf = os.path.abspath(f"orcamento_{orcamento_id}_temp.pdf")
        caminho_logo = os.path.abspath("fence.logo1.png")
        try:
            with SessionLocal() as session:
                orcamento = session.query(Orcamento).options(joinedload(
                    Orcamento.cliente)).filter(Orcamento.id == orcamento_id).first()
                if not orcamento:
                    raise ValueError("Orçamento não encontrado.")

                gerar_orcamento(orcamento, caminho_pdf)

                assunto = f"Fence Estimate Nº {orcamento.id} - Nunes Fence LLC"
                corpo_html = criar_corpo_html_orcamento(orcamento)

                # MUDANÇA 2: Chamando a função correta (enviar_email_smtp)
                enviar_email_smtp(
                    destinatario=orcamento.cliente.email,
                    assunto=assunto,
                    corpo_html=corpo_html,
                    caminho_anexo=caminho_pdf,
                    caminho_imagem_embutida=caminho_logo
                )

            fila.put("SUCESSO")

        except Exception as e:
            # Imprime o erro no terminal para facilitar a depuração
            print("\n\n--- [!!! WORKER ERROR !!!] ---")
            traceback.print_exc()
            print("-----------------------------\n")
            fila.put(e)

        finally:
            if os.path.exists(caminho_pdf):
                os.remove(caminho_pdf)

    def verificar_fila_de_resultados(self):
        """
        Verifica a fila de resultados sem bloquear a interface.
        Atualiza o status na tela quando a tarefa em segundo plano termina.
        """
        try:
            # Tenta obter um item da fila.
            resultado = self.resultado_fila.get_nowait()

            if resultado == "SUCESSO":
                orcamento_id = self.tree.item(
                    self.tree.selection(), "values")[0]
                self.status_label.configure(
                    text=f"E-mail para o orçamento {orcamento_id} enviado!", text_color="lightgreen")
            else:
                # Se o resultado for uma exceção, lança o erro.
                raise resultado

        except queue.Empty:
            # Se a fila estiver vazia, a tarefa ainda está em andamento.
            # Agenda a próxima verificação para daqui a 100ms.
            self.after(100, self.verificar_fila_de_resultados)

        except Exception as e:
            # Se um erro foi pego da fila, exibe na tela.
            self.status_label.configure(
                text=f"Erro ao enviar: {e}", text_color="red")

        finally:
            # Se a fila não está vazia, significa que o processo terminou.
            if not self.resultado_fila.empty():
                self.after(7000, lambda: self.status_label.destroy())

    def submit_cliente(self):
        """Handler para cadastrar cliente a partir da GUI (aba Cadastrar Cliente)."""
        nome = self.entry_nome_cliente.get().strip()
        email = self.entry_email_cliente.get().strip()
        telefone = self.entry_telefone_cliente.get().strip()
        endereco = self.entry_endereco_cliente.get().strip()

        if not nome:
            self.client_create_status_label.configure(
                text="Erro: Nome é obrigatório.", text_color="red")
            return

        try:
            with SessionLocal() as session:
                cliente = cadastrar_cliente(
                    nome=nome, telefone=telefone, endereco=endereco, email=email, db=session)
            self.client_create_status_label.configure(
                text=f"Cliente cadastrado (ID: {cliente.id})", text_color="green")
            # limpa campos
            self.entry_nome_cliente.delete(0, ctk.END)
            self.entry_email_cliente.delete(0, ctk.END)
            self.entry_telefone_cliente.delete(0, ctk.END)
            self.entry_endereco_cliente.delete(0, ctk.END)
            # atualiza a lista de clientes na aba Clientes
            self.carregar_clientes()
        except ValueError as ve:
            self.client_create_status_label.configure(
                text=f"Erro: {ve}", text_color="red")
        except Exception as e:
            self.client_create_status_label.configure(
                text=f"Erro ao cadastrar: {e}", text_color="red")


if __name__ == "__main__":
    app = App()
    app.mainloop()
