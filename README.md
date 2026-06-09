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

O **PDV Notas** é um sistema desktop simples e direto, projetado para funcionar como um Ponto de Venda (PDV) para emissão de notas ou cupons não fiscais e controle de estoque básico. Com foco em pequenos comércios ou prestadores de serviços autônomos, o aplicativo oferece uma interface limpa para registrar vendas, gerenciar o histórico, cadastrar produtos e emitir comprovantes impressos de forma ágil.

*Nota: Este projeto possui fins de estudo e facilitação de fluxos simples, e os cupons gerados não possuem validade fiscal (NFC-e/SAT).*

<!-- Placeholder para uma futura screenshot -->
<!-- <p align="center"><img src="./assets/screenshot.png" alt="Tela Principal do Sistema" width="600"></p> -->

---

## 🚀 Funcionalidades

- **[+] Novo Cadastro de Nota:** 
  - Inserção ágil de itens, com campos para valor unitário e quantidade.
  - Cálculo automático de subtotal por item.
  - Agrupamento inteligente de múltiplos itens na mesma nota/venda.
- **[📦] Controle de Estoque:**
  - Tela dedicada para o registro (cadastro) de produtos no sistema.
  - Visualização (listagem) de todos os itens cadastrados no estoque.
  - Edição e exclusão de itens diretamente pela interface de listagem (CRUD Completo).
  - Armazenamento de código, descrição, valor e quantidade em estoque.
- **[🔎] Consulta de Vendas:**
  - Visualização em tabela de todo o histórico de vendas registrado no sistema.
- **[🖨️] Emissão e Visualização de Comprovante:**
  - Interface para seleção de nota específica através de lista.
  - Tabela de pré-visualização da nota na interface antes da impressão.
  - Geração de layout de "Cupom" estruturado em texto plano (`.txt`).
  - Envio automatizado para a fila de impressão padrão do sistema operacional, facilitando o uso com impressoras térmicas genéricas.

---

## 🛠️ Tecnologias

As seguintes ferramentas e bibliotecas foram utilizadas na construção do projeto:

- **[Python](https://www.python.org/):** Linguagem core da aplicação.
- **[PySimpleGUI](https://pysimplegui.readthedocs.io/):** Responsável por abstrair bibliotecas gráficas complexas e entregar a interface do usuário.
- **[SQLite3](https://docs.python.org/3/library/sqlite3.html):** Banco de dados relacional embarcado, garantindo que o software funcione de maneira portátil, sem necessidade de instalar um servidor de banco de dados (ex: MySQL, PostgreSQL).

---

## 📂 Arquitetura

Para manter o código limpo, escalável e de fácil manutenção, o projeto foi estruturado seguindo os princípios do padrão **MVC (Model-View-Controller)** adaptado para desktop:

```text
Projeto 2 com UI/
├── App/
│   ├── Banco/             # Arquivo do banco de dados SQLite persistente (base.db)
│   ├── Controller/        # Intermediários: Capturam eventos da View e chamam as regras de negócio
│   │   ├── CadastrarNotaController.py
│   │   ├── CadastroEstoqueController.py
│   │   ├── ListarEstoqueController.py
│   │   └── ListarNotaController.py
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

# Instale as dependências (PySimpleGUI)
$ pip install PySimpleGUI

# Execute a aplicação
$ python main.py
```

---

## 🗺️ Roadmap (Próximos Passos)

Como o projeto está em desenvolvimento contínuo, aqui estão algumas melhorias mapeadas para o futuro:

- [x] Criação de uma tela de gerenciamento de Produtos (Cadastro de Estoque).
- [x] Criação de uma tela para visualização de Produtos (Listagem de Estoque).
- [x] Implementação de edição e exclusão de Produtos (CRUD Completo).
- [ ] Implementação de dashboard com gráficos básicos de faturamento diário/mensal.
- [ ] Exportação do histórico de vendas para Excel/CSV.
- [ ] Opção de configurar os dados do estabelecimento pela interface.

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
