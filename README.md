# 📊 Sistema de Geração de Orçamentos

![status](https://img.shields.io/badge/status-Em%20Desenvolvimento-yellow)
![python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![tests](https://img.shields.io/badge/Tests-Passing-brightgreen?logo=pytest)
![license](https://img.shields.io/badge/Licen%C3%A7a-MIT-green)

> **Nota:** Este projeto está em fase de desenvolvimento. O objetivo é criar uma aplicação de desktop completa para a gestão de orçamentos, com foco em código de qualidade, testável e de fácil manutenção.

## 📖 Descrição do Projeto

O **Sistema de Geração de Orçamentos** será uma aplicação de desktop desenvolvida em Python para auxiliar profissionais autônomos e pequenas empresas a otimizar o processo de criação e gerenciamento de propostas comerciais. A ferramenta permitirá cadastrar clientes, definir um catálogo de serviços e gerar orçamentos de forma rápida e organizada.

## 💡 Motivação

A inspiração para este projeto veio de uma dificuldade real que vivenciei. Durante o período em que geri minha própria empresa nos Estados Unidos, percebi que a maioria das ferramentas para criação de orçamentos era ou complexa demais para as minhas necessidades, ou baseada em assinaturas mensais que não se justificavam para um pequeno negócio.

Senti falta de uma solução de desktop simples, rápida, offline e sem custos recorrentes.

Este sistema é a minha resposta a esse problema: uma ferramenta prática, construída para resolver uma dor que eu, como empreendedor, senti na pele. É um projeto que une minha experiência passada em negócios com minha nova paixão por desenvolver soluções com software.

## ✨ Funcionalidades Planejadas

-   [ ] **Gerenciamento de Clientes:** CRUD completo para a base de clientes.
-   [ ] **Catálogo de Serviços:** CRUD completo para produtos e serviços.
-   [ ] **Criação e Gestão de Orçamentos:** Geração de propostas associando clientes e serviços.
-   [ ] **Interface Gráfica Intuitiva:** Interface de usuário (GUI) a ser desenvolvida com CustomTkinter.
-   [ ] **Histórico e Busca:** Visualização e busca de orçamentos já criados.

## 🛠️ Tecnologias Utilizadas

-   **Linguagem Principal:** Python 3
-   **Banco de Dados:** SQLite 3
-   **Testes:** Pytest
-   **Interface Gráfica (Planejada):** CustomTkinter

## ✅ Testes

A qualidade do código é uma prioridade neste projeto. A suíte de testes automatizados garante a estabilidade e o correto funcionamento da lógica de negócios.

Para executar os testes, utilize o seguinte comando na raiz do projeto:

python -m pytest

## 🚀 Como Rodar o Projeto

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/andrelsrn/sistema-orcamento.git](https://github.com/andrelsrn/sistema-orcamento.git)
    ```
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
5.  **Execute a aplicação (quando a UI for implementada):**
    ```bash
    python src/main.py
    ```

## 👤 Autor

**André Nunes**

-   GitHub: [@andrelsrn](https://github.com/andrelsrn)
-   LinkedIn: [@andre-nunes-03866b55](https://www.linkedin.com/in/andre-nunes-03866b55/)