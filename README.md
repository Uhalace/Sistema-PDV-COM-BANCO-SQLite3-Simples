<h1 align="center">
  <img src="./Icones/nota.jpg" alt="Logo PDV Notas" width="120" style="border-radius: 20%;"><br>
  PDV Notas
</h1>

<p align="center">
  <a href="#-sobre-o-projeto">Sobre</a> •
  <a href="#-funcionalidades">Funcionalidades</a> •
  <a href="#%EF%B8%8F-tecnologias">Tecnologias</a> •
  <a href="#-arquitetura">Arquitetura</a> •
  <a href="#-como-executar">Como Executar</a> •
  <a href="#-roadmap-próximos-passos">Roadmap</a>
</p>

<p align="center">
  <img alt="Status do Projeto" src="https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow?style=for-the-badge">
  <img alt="Linguagem Principal" src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img alt="Banco de Dados" src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white">
</p>

---

## 💻 Sobre o Projeto

O **PDV Notas** é um sistema desktop ágil e direto, projetado para atuar como um Ponto de Venda (PDV) com foco em emissão de notas/cupons não fiscais e controle de estoque integrado. Voltado para pequenos comércios ou prestadores de serviços, o aplicativo oferece uma interface limpa para realizar vendas, abater o estoque automaticamente, gerenciar produtos e emitir comprovantes impressos.

*Nota: Este projeto possui fins de estudo e facilitação de fluxos simples comerciais. Os cupons gerados não possuem validade fiscal (NFC-e/SAT).*

---

## 🚀 Funcionalidades

- **[+] Ponto de Venda Integrado (Cadastro de Nota):** 
  - **Busca Rápida:** Integração direta com o estoque. Digite o código do produto e busque para preencher automaticamente o nome e o valor.
  - **Baixa de Estoque Automática:** Ao salvar uma venda, o sistema verifica o saldo e deduz automaticamente a quantidade vendida do estoque do produto. Alerta caso haja saldo insuficiente.
  - Inserção ágil de itens com cálculo automático de subtotal por item.
  - Agrupamento inteligente de múltiplos itens na mesma nota/venda.
  - Botão de atalho para **Imprimir Nota** logo após finalizar a venda, sem precisar sair da tela.

- **[📦] Gestão Completa de Estoque (CRUD):**
  - **Cadastro:** Tela dedicada para o registro de novos produtos no sistema.
  - **Listagem e Consulta:** Visualização em tabela de todos os itens cadastrados no estoque, com paginação para melhor performance.
  - **Edição e Exclusão:** Gestão completa dos itens, sendo possível editar os valores e quantidades ou remover um item clicando na tabela.
  - Armazenamento estruturado de código, descrição, valor e quantidade.

- **[🔎] Consulta de Vendas:**
  - Visualização em tabela do histórico completo das vendas registradas.

- **[🖨️] Emissão e Visualização de Comprovante:**
  - Interface para seleção de nota específica por número.
  - Tabela de pré-visualização da nota e conferência do total antes da impressão.
  - Geração de um layout de "Cupom" perfeitamente estruturado em texto plano (`.txt`).
  - Envio automatizado para a fila de impressão padrão do sistema operacional, ideal para impressoras térmicas genéricas (Não-Fiscais).

- **[📊] Relatórios e Gráficos:**
  - **Relatório de Vendas:** Resumo financeiro contendo faturamento total, quantidade de itens vendidos e o total de notas registradas, exibido em uma tabela detalhada.
  - **Relatório de Estoque:** Visão geral do inventário com soma da quantidade de itens e o valor total acumulado no estoque.
  - **Exportação para CSV:** Geração de arquivos CSV com o histórico de vendas e dados do estoque para abertura em planilhas eletrônicas.
  - **Gráficos Interativos:** Geração de gráficos no navegador web usando Plotly para visualização de métricas como "Faturamento por Item" e "Quantidade em Estoque por Item".

- **[🏢] Cadastro de Estabelecimento:**
  - Interface dedicada para o registro dos dados da empresa/estabelecimento.
  - Personalização das informações para o sistema.

---

## 🛠️ Tecnologias

As seguintes ferramentas e bibliotecas foram utilizadas na construção do projeto:

- **[Python](https://www.python.org/):** Linguagem core da aplicação.
- **[PySimpleGUI](https://pysimplegui.readthedocs.io/):** Responsável por abstrair bibliotecas gráficas complexas e entregar a interface do usuário fluida e ágil.
- **[SQLite3](https://docs.python.org/3/library/sqlite3.html):** Banco de dados relacional embarcado, garantindo que o software funcione de maneira portátil, sem necessidade de instalar um servidor de banco de dados (ex: MySQL, PostgreSQL).
- **[Pandas](https://pandas.pydata.org/):** Utilizado para manipulação de dados em tabelas para os relatórios.
- **[Plotly](https://plotly.com/python/):** Responsável por gerar os gráficos interativos dinâmicos que podem ser visualizados no navegador.

---

## 📂 Arquitetura

Para manter o código limpo, escalável e de fácil manutenção, o projeto foi estruturado seguindo os princípios do padrão **MVC (Model-View-Controller)** adaptado para desktop:

```text
Projeto 2 com UI/
├── App/
│   ├── Banco/             # Arquivo do banco de dados SQLite persistente (base.db) e gráficos .html
│   ├── Controller/        # Intermediários: Capturam eventos da View e chamam as regras de negócio
│   │   ├── CadastrarNotaController.py
│   │   ├── CadastroEstoqueController.py
│   │   ├── ListarEstoqueController.py
│   │   ├── ListarNotaController.py
│   │   ├── RelatorioEstoqueController.py
│   │   └── RelatorioVendasController.py
│   ├── Functions/         # Helpers e utilitários globais (ex: formatação de moeda R$)
│   └── Model/             # Camada de Dados: Conexão e queries SQL encapsuladas
│       └── Banco.py
├── App/app.py             # View principal e inicialização das telas
├── Icones/                # Recursos de mídia (ícones da janela, logo)
└── main.py                # Ponto de entrada (Entrypoint)
```

---

## ⚙️ Como Executar

Siga os passos abaixo para rodar o projeto no seu ambiente local.

### 1. Pré-requisitos
Certifique-se de ter o **Python 3.x** instalado na sua máquina. Verifique abrindo o terminal e digitando:
```bash
python --version
```

### 2. Passo a Passo

```bash
# Clone este repositório
$ git clone <link-do-seu-repositorio>

# Acesse a pasta do projeto no terminal/cmd
$ cd "Projeto 2 com UI"

# (Opcional, mas recomendado) Crie um ambiente virtual
$ python -m venv venv

# Ative o ambiente virtual
# No Windows:
$ venv\Scripts\activate
# No Linux/MacOS:
$ source venv/bin/activate

# Instale as dependências (PySimpleGUI, Pandas, Plotly)
$ pip install PySimpleGUI pandas plotly

# Execute a aplicação
$ python main.py
```

---

## 🗺️ Roadmap (Próximos Passos)

Como o projeto está em desenvolvimento contínuo, aqui estão algumas melhorias mapeadas para o futuro:

- [x] Criação de uma tela de gerenciamento de Produtos (Cadastro de Estoque).
- [x] Criação de uma tela para visualização de Produtos (Listagem de Estoque).
- [x] Implementação de edição e exclusão de Produtos (CRUD Completo).
- [x] Integração da Tela de Vendas com o Estoque (Baixa automática e busca de código).
- [x] Exportação do histórico de vendas e de estoque para CSV.
- [x] Implementação de gráficos básicos (Faturamento por item e Estoque por item).
- [x] Implementação de gráficos de faturamento diário/mensal.
- [x] Opção de configurar os dados do estabelecimento pela interface.

---

## 🤝 Contribuição

Sinta-se à vontade para contribuir com o projeto! Se você encontrar algum bug ou tiver uma ideia de funcionalidade:

1. Faça um **Fork** do projeto.
2. Crie uma nova branch com a sua feature: `git checkout -b minha-feature`
3. Faça commit das suas alterações: `git commit -m 'Feat: Minha nova feature'`
4. Faça push para a branch: `git push origin minha-feature`
5. Abra um **Pull Request**.

---

<p align="center">
  Desenvolvido com dedicação por <b>Uhalace de Souza</b>.
</p>
