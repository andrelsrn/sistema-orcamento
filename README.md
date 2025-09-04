# 📊 Sistema de Geração de Orçamentos

[![status](https://img.shields.io/badge/status-Ativo-brightgreen)]()
[![python](https://img.shields.io/badge/Python-3.10-blue?logo=python)]()
[![tests](https://img.shields.io/badge/Tests-Passing-brightgreen?logo=pytest)]()
[![coverage](https://img.shields.io/badge/coverage-87%25-brightgreen)]()
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)



> **Sistema completo de geração de orçamentos com GUI em Python, exportação em PDF e envio automático por e-mail.**  
> Código limpo, testável e fácil manutenção, pronto para uso profissional.

---

## 📖 Descrição do Projeto

O **Sistema de Geração de Orçamentos** é uma ferramenta em Python para auxiliar profissionais autônomos e pequenas empresas a otimizar o processo de criação e gerenciamento de propostas comerciais.  

Permite cadastrar clientes, gerenciar orçamentos, gerar PDFs e enviar e-mails automaticamente, tudo de forma rápida, organizada e profissional.

---

## 📸 Demonstração

### 🖥️ CLI - Cadastro de Cliente
![Exemplo CLI - Cadastro de Cliente](https://raw.githubusercontent.com/andrelsrn/sistema-orcamento/main/src/images/cadastro-cli.png)

### 🖥️ CLI - Cadastro de Orçamento
![Exemplo CLI - Geração de Orçamento](https://raw.githubusercontent.com/andrelsrn/sistema-orcamento/main/src/images/gerador-orcamento.png)

### 🪟 Interface Gráfica (GUI)
Interface desenvolvida com **CustomTkinter**, totalmente funcional e integrada a todas as funcionalidades do sistema.

![Exemplo GUI - V.1](https://raw.githubusercontent.com/andrelsrn/sistema-orcamento/main/src/images/demo-gui_.png)

🎥 [Assista ao vídeo demonstrativo da GUI](https://youtu.be/rDGvQf-u_Fk)

### 📄 Exemplo de Proposta em PDF
Print de um orçamento gerado automaticamente pelo sistema (proposta fictícia):

![Exemplo PDF - Proposta](https://raw.githubusercontent.com/andrelsrn/sistema-orcamento/main/src/images/demo-pdf.png)

---

## 💡 Motivação

Durante minha experiência como empreendedor nos EUA, percebi que as ferramentas de orçamento eram complexas ou caras demais para pequenos negócios.  
Este projeto é minha solução prática, rápida e offline, unindo minha experiência de negócios à programação em Python.

---

## ✨ Funcionalidades

### Backend
- [x] CRUD completo de clientes e orçamentos  
- [x] Geração de PDFs de propostas  
- [x] Envio automático de e-mails via SMTP/HTML

### GUI
- [x] Interface em **CustomTkinter**, versão inicial concluída e totalmente funcional  
- [x] Histórico e busca de orçamentos  

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.10**  
- **Banco de Dados:** SQLite 3 com **SQLAlchemy**  
- **Interface Gráfica:** **CustomTkinter**  
- **Geração de PDF:** **ReportLab**  
- **Testes:** **Pytest**  
- **Envio de E-mails:** SMTP (Gmail) com corpo em HTML  

---


## ✅ Testes

A qualidade do código é uma prioridade neste projeto. A suíte de testes automatizados garante a estabilidade e o correto funcionamento da lógica de negócios.

Para executar os testes, utilize o seguinte comando na raiz do projeto:

```bash
pip install -r requirements-dev.txt
python -m pytest
```

## 🚀 Como Rodar o Projeto

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/andrelsrn/sistema-orcamento.git](https://github.com/andrelsrn/sistema-orcamento.git)
    ```
    *Observação: Lembre-se de atualizar para a URL correta do seu repositório.*

2.  **Navegue até a pasta do projeto:**
    ```bash
    cd sistema-orcamento
    ```
3.  **Crie e ative um ambiente virtual:**
    ```bash
    # Crie o ambiente
    python -m venv .venv
    # Ative o ambiente (Windows)
    .venv\Scripts\activate
    # Ative o ambiente (Linux/Mac)
    # source .venv/bin/activate
    ```
4.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Execute a aplicação:**
    ```bash
    python src/main.py
    ```

## 🛣️ Roadmap

- [ ] Refinamento do design da interface gráfica (CustomTkinter).  
- [ ] Implementação de temas customizáveis (ex: dark mode).  
- [ ] Integração com API de envio de e-mails (ex: SendGrid, AWS SES).  
- [ ] Empacotamento da aplicação em executável (.exe / .app) para distribuição.  
- [ ] Deploy de versão web (FastAPI + frontend).  


## 👨‍💻 Autor

Desenvolvido por **André Nunes**  

🔗 [LinkedIn](https://www.linkedin.com/in/andre-nunes-03866b55/) | [GitHub](https://github.com/andrelsrn)  

💡 Desenvolvedor backend em Python, com experiência em automação, geração de relatórios e aplicações desktop.  
Ex-empreendedor nos EUA, aplico minha vivência de negócios para criar soluções de software que resolvem problemas reais.

---


## 📜 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
