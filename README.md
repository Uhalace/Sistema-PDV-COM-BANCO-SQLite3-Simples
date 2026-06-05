# PDV Notas

![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow)

O **PDV Notas** é um sistema de Ponto de Venda (PDV) desktop simples desenvolvido em Python. Ele permite o cadastro, listagem e impressão de notas/cupons não fiscais de forma rápida e intuitiva.

## 🚀 Funcionalidades

- **Cadastrar Notas:** Adição de itens, quantidades e valores, com cálculo automático de subtotais e controle por número de nota.
- **Listar Vendas:** Visualização do histórico completo de vendas cadastradas no sistema.
- **Imprimir Nota:** Geração de um "Cupom Fiscal" (sem validade fiscal) em formato de texto (`.txt`) e envio direto para a fila de impressão padrão do sistema operacional.

## 🛠️ Tecnologias Utilizadas

- **Python:** Linguagem principal do projeto.
- **[PySimpleGUI](https://pysimplegui.readthedocs.io/):** Biblioteca utilizada para a construção da Interface Gráfica de Usuário (GUI).
- **SQLite3:** Banco de dados relacional leve embutido utilizado para armazenar as vendas de forma persistente e local.

## 📁 Estrutura do Projeto

O projeto segue um padrão de arquitetura baseado em **MVC (Model-View-Controller)** para melhor organização do código:

```
Projeto 2 com UI/
├── App/
│   ├── Banco/             # Arquivo do banco de dados SQLite (base.db)
│   ├── Controller/        # Regras de negócio e integração UI/Banco (Cadastrar, Listar)
│   ├── Functions/         # Funções auxiliares (ex: formatação monetária)
│   └── Model/             # Conexão e operações CRUD com o banco de dados (Banco.py)
├── Icones/                # Ícones utilizados na interface do usuário
└── main.py                # Ponto de entrada da aplicação
```

## ⚙️ Como Executar o Projeto

### Pré-requisitos

- **Python 3.x** instalado na sua máquina.

### Passos para rodar localmente

1. Clone ou faça o download deste repositório para a sua máquina.
2. Navegue até a pasta raiz do projeto via terminal.
3. (Opcional) Recomenda-se criar um ambiente virtual (venv):
   ```bash
   python -m venv venv
   # Ative no Windows:
   venv\Scripts\activate
   # Ative no Linux/Mac:
   source venv/bin/activate
   ```
4. Instale as dependências necessárias. Você precisará instalar o PySimpleGUI:
   ```bash
   pip install PySimpleGUI
   ```
5. Execute o arquivo principal da aplicação:
   ```bash
   python main.py
   ```

## ⚠️ Status do Projeto

Este projeto **ainda está em desenvolvimento**. Novas funcionalidades e melhorias de código estão sendo implementadas.

## 👨‍💻 Autor

Desenvolvido por **Uhalace de Souza**.
