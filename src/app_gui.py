import customtkinter as ctk
from .db import SessionLocal
from .services.cliente_service import buscar_cliente_por_nome as service_buscar_cliente_por_nome

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Orçamentos de Cerca")
        self.geometry("800x600")

        # Define o tema
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # Dados do formulário
        self.materiais_data = {
            "Madeira": ["6x6", "6x8"],
            "Alumínio": ["4x6", "5x6"],
            "PVC": ["6x6", "6x8"]
        }
        
        # Lista para guardar widgets de portão dinâmicos
        self.gate_widgets = []

        # Cria a barra de abas
        self.tab_view = ctk.CTkTabview(self, width=780)
        self.tab_view.pack(padx=10, pady=10, fill="both", expand=True)

        self.tab_view.add("Cadastrar Orçamento")
        self.tab_view.add("Consultar Orçamentos")
        self.tab_view.add("Clientes")

        # --- Aba: Cadastrar Orçamento ---
        self.tab_1_frame = self.tab_view.tab("Cadastrar Orçamento")
        self.tab_1_frame.grid_columnconfigure(1, weight=1)

        # -- Cliente --
        self.client_label = ctk.CTkLabel(self.tab_1_frame, text="Nome do Cliente:")
        self.client_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        self.client_entry = ctk.CTkEntry(self.tab_1_frame, placeholder_text="Digite o nome para buscar...")
        self.client_entry.grid(row=0, column=1, padx=20, pady=(20, 10), sticky="ew")

        # -- Material --
        self.material_label = ctk.CTkLabel(self.tab_1_frame, text="Material:")
        self.material_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.material_combobox = ctk.CTkComboBox(self.tab_1_frame, values=list(self.materiais_data.keys()), command=self.update_panel_sizes)
        self.material_combobox.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

        # -- Tamanho do Painel --
        self.panel_label = ctk.CTkLabel(self.tab_1_frame, text="Tamanho do Painel:")
        self.panel_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.panel_combobox = ctk.CTkComboBox(self.tab_1_frame, values=[]) # Começa vazio
        self.panel_combobox.grid(row=2, column=1, padx=20, pady=10, sticky="ew")

        # -- Cor --
        self.color_label = ctk.CTkLabel(self.tab_1_frame, text="Cor do Material (PVC):")
        self.color_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        self.color_combobox = ctk.CTkComboBox(self.tab_1_frame, values=["Branco", "Bege", "Marrom", "Cinza"])
        self.color_combobox.grid(row=3, column=1, padx=20, pady=10, sticky="ew")

        # -- Metragem --
        self.footage_label = ctk.CTkLabel(self.tab_1_frame, text="Metragem (metros):")
        self.footage_label.grid(row=4, column=0, padx=20, pady=10, sticky="w")
        self.footage_entry = ctk.CTkEntry(self.tab_1_frame, placeholder_text="Ex: 50.5")
        self.footage_entry.grid(row=4, column=1, padx=20, pady=10, sticky="ew")

        # -- Portão --
        self.gate_check = ctk.CTkCheckBox(self.tab_1_frame, text="Adicionar Portão?", command=self.toggle_gate_fields)
        self.gate_check.grid(row=5, column=0, padx=20, pady=10, sticky="w")

        # Widgets do portão (visibilidade controlada por toggle_gate_fields)
        self.gate_qty_label = ctk.CTkLabel(self.tab_1_frame, text="Quantidade de Portões:")
        self.gate_qty_entry = ctk.CTkEntry(self.tab_1_frame, placeholder_text="Ex: 1")
        self.gate_qty_entry.bind("<KeyRelease>", self.update_gate_fields)

        # Frame para os campos de tamanho de portão dinâmicos
        self.gate_sizes_frame = ctk.CTkScrollableFrame(self.tab_1_frame, label_text="Tamanhos dos Portões")
        
        # -- Botão de Cadastro --
        self.submit_button = ctk.CTkButton(self.tab_1_frame, text="Cadastrar Orçamento", command=self.submit_form)
        self.submit_button.grid(row=9, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

        # Conteúdo das outras abas
        self.label_tab2 = ctk.CTkLabel(self.tab_view.tab("Consultar Orçamentos"), text="Lista de Orçamentos aqui.")
        self.label_tab2.pack(padx=20, pady=20)

        self.label_tab3 = ctk.CTkLabel(self.tab_view.tab("Clientes"), text="Gerenciamento de Clientes aqui.")
        self.label_tab3.pack(padx=20, pady=20)
        
        # --- Inicialização dos estados dos widgets ---
        self.update_panel_sizes(self.material_combobox.get())
        self.toggle_gate_fields()

    def update_panel_sizes(self, material: str):
        """Atualiza as opções do combobox de tamanho de painel com base no material."""
        panel_sizes = self.materiais_data.get(material, [])
        self.panel_combobox.configure(values=panel_sizes)
        if panel_sizes:
            self.panel_combobox.set(panel_sizes[0])
        else:
            self.panel_combobox.set("")

    def toggle_gate_fields(self):
        """Mostra ou esconde os campos de quantidade e o frame dos tamanhos."""
        if self.gate_check.get() == 1:
            self.gate_qty_label.grid(row=6, column=0, padx=20, pady=10, sticky="w")
            self.gate_qty_entry.grid(row=6, column=1, padx=20, pady=10, sticky="ew")
            self.gate_sizes_frame.grid(row=7, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
            self.update_gate_fields()
        else:
            self.gate_qty_label.grid_forget()
            self.gate_qty_entry.grid_forget()
            self.gate_sizes_frame.grid_forget()
            self.update_gate_fields()

    def update_gate_fields(self, event=None):
        """Cria campos de tamanho de portão dinamicamente com base na quantidade."""
        for widget in self.gate_widgets:
            widget.destroy()
        self.gate_widgets.clear()

        try:
            qty = int(self.gate_qty_entry.get())
        except ValueError:
            qty = 0

        for i in range(qty):
            gate_size_label = ctk.CTkLabel(self.gate_sizes_frame, text=f"Tamanho do Portão {i+1}:")
            gate_size_label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
            self.gate_widgets.append(gate_size_label)

            gate_size_combobox = ctk.CTkComboBox(self.gate_sizes_frame, values=["Single", "Double"])
            gate_size_combobox.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            self.gate_widgets.append(gate_size_combobox)

    def submit_form(self):
        """Lê os dados do formulário, busca o cliente no DB e imprime o resultado."""
        print("--- Buscando Cliente no Banco de Dados ---")
        
        client_name = self.client_entry.get()
        
        if not client_name:
            print("Erro: Nome do cliente não pode estar vazio.")
            return

        print(f"Buscando por: '{client_name}'")

        try:
            with SessionLocal() as session:
                clientes_encontrados = service_buscar_cliente_por_nome(client_name, db=session)
            
            if clientes_encontrados:
                print("Clientes encontrados:")
                for cliente in clientes_encontrados:
                    print(f"  - ID: {cliente.id}, Nome: {cliente.nome}")
            else:
                print("Nenhum cliente encontrado com esse nome.")

        except Exception as e:
            print(f"Ocorreu um erro ao buscar o cliente: {e}")

        print("-----------------------------------------")

if __name__ == "__main__":
    app = App()
    app.mainloop()
