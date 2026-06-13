import os
import sqlite3
import logging
from datetime import datetime, timedelta

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Banco:
    """Gerenciador de banco de dados SQLite para o PDV Notas"""
    
    def __init__(self):
        """Inicializa conexão com banco de dados e cria tabelas se necessário"""
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.abspath(os.path.join(base_dir, '..', 'Banco', 'base.db'))
            os.makedirs(os.path.dirname(db_path), exist_ok=True)

            self.conexao = sqlite3.connect(db_path)
            self.conexao.execute("PRAGMA foreign_keys = ON")  # Habilitar integridade referencial
            self.cursor = self.conexao.cursor()
            logger.info(f"Banco de dados conectado: {db_path}")
        except Exception as e:
            logger.error(f"Erro ao conectar ao banco de dados: {e}")
            raise
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_nota INTEGER NOT NULL,
                item TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                valor INTEGER NOT NULL,
                subtotal INTEGER NOT NULL,
                data_cadastro TEXT DEFAULT (DATE('now')),
                UNIQUE(numero_nota, item)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS estoque (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo INTEGER NOT NULL UNIQUE,
                item VARCHAR(250) NOT NULL,
                quantidade INTEGER NOT NULL DEFAULT 0,
                valor INTEGER NOT NULL,
                data_cadastro TEXT DEFAULT (DATE('now')),
                CHECK(quantidade >= 0)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS estabelecimento (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(250) NOT NULL,
                CNPJ VARCHAR(250),
                telefone VARCHAR(250),
                IE VARCHAR(250),
                endereco VARCHAR(250),
                data_cadastro TEXT DEFAULT (DATE('now'))
            )
        """)
        self.conexao.commit()
        logger.info("Tabelas criadas ou já existentes")

    def inserir_venda(self, numero_nota, item, quantidade, valor, subtotal):
        """Insere uma venda no banco de dados com validação"""
        try:
            if not all([numero_nota, item, quantidade, valor, subtotal]):
                raise ValueError("Todos os campos são obrigatórios")
            
            self.cursor.execute("""
                INSERT INTO vendas (numero_nota, item, quantidade, valor, subtotal)
                VALUES (?, ?, ?, ?, ?)
            """, (numero_nota, item, quantidade, valor, subtotal))
            self.conexao.commit()
            logger.info(f"Venda inserida: Nota {numero_nota}, Item: {item}")
            return True
        except sqlite3.IntegrityError as e:
            logger.error(f"Erro de integridade ao inserir venda: {e}")
            raise ValueError(f"Este item já foi adicionado a esta nota")
        except Exception as e:
            logger.error(f"Erro ao inserir venda: {e}")
            raise

    def listar_vendas(self):
        self.cursor.execute("SELECT * FROM vendas")
        return self.cursor.fetchall()

    def imprimir_nota(self, numero_nota):
        self.cursor.execute("SELECT * FROM vendas WHERE numero_nota = ?", (numero_nota,))
        return self.cursor.fetchall()

    def obter_vendas_por_nota(self, numero_nota):
        return self.imprimir_nota(numero_nota)

    def numero_nota_bd(self):
        self.cursor.execute("SELECT MAX(numero_nota) FROM vendas")
        resultado = self.cursor.fetchone()
        return resultado[0] + 1 if resultado[0] is not None else 1
    
    def listar_numeros_notas(self):
        self.cursor.execute("SELECT DISTINCT numero_nota FROM vendas")
        return [row[0] for row in self.cursor.fetchall()]
    
    # Métodos para o estoque
    def inserir_estoque(self, codigo, item, quantidade, valor):
        self.cursor.execute("""
            INSERT INTO estoque (codigo, item, quantidade, valor)
            VALUES (?, ?, ?, ?)
        """, (codigo, item, quantidade, valor))
        self.conexao.commit()
    # BUSCANDO ITEM CADASTRADO
    def Bucar_item(self, codigo):
        """Busca um item no estoque pelo código"""
        try:
            self.cursor.execute("SELECT * FROM estoque WHERE codigo = ?", (codigo,))
            resultado = self.cursor.fetchone()
            if resultado:
                logger.info(f"Produto encontrado: {codigo}")
            return resultado
        except Exception as e:
            logger.error(f"Erro ao buscar item {codigo}: {e}")
            return None
    
    def buscar_item_por_nome(self, nome):
        """Busca um item no estoque pelo nome (parcial)"""
        try:
            self.cursor.execute("SELECT * FROM estoque WHERE item LIKE ? LIMIT 1", (f"%{nome}%",))
            resultado = self.cursor.fetchone()
            return resultado
        except Exception as e:
            logger.error(f"Erro ao buscar item por nome {nome}: {e}")
            return None
    
    #DAR BAIXA ESTOQUE 
    def dar_baixa_estoque(self, codigo, quantidade):
        """Reduz quantidade do estoque e retorna sucesso"""
        try:
            # Verifica se o item existe e se há saldo suficiente antes de decrementar
            self.cursor.execute(
                "SELECT id, quantidade FROM estoque WHERE codigo = ? AND quantidade >= ?",
                (codigo, quantidade)
            )
            row = self.cursor.fetchone()
            
            if not row:
                logger.warning(f"Estoque insuficiente para código {codigo}")
                return False
            
            id_estoque = row[0]
            quantidade_atual = row[1]
            
            if quantidade_atual >= quantidade:
                self.cursor.execute(
                    "UPDATE estoque SET quantidade = quantidade - ? WHERE id = ?",
                    (quantidade, id_estoque)
                )
                self.conexao.commit()
                logger.info(f"Estoque reduzido: Código {codigo}, Quantidade: {quantidade}")
                return True
            else:
                logger.warning(f"Quantidade insuficiente para código {codigo}")
                return False
        except Exception as e:
            logger.error(f"Erro ao dar baixa no estoque {codigo}: {e}")
            return False
    #LISTAR ESTOQUE
    def listar_estoque(self):
        """Lista todos os itens do estoque"""
        try:
            self.cursor.execute("SELECT id, codigo, item, quantidade, valor FROM estoque")
            return self.cursor.fetchall()
        except Exception as e:
            logger.error(f"Erro ao listar estoque: {e}")
            return []

    def atualizar_estoque(self, id, codigo, item, quantidade, valor):
        """Atualiza um item do estoque"""
        try:
            self.cursor.execute("""
                UPDATE estoque
                SET codigo = ?, item = ?, quantidade = ?, valor = ?
                WHERE id = ?
            """, (codigo, item, quantidade, valor, id))
            self.conexao.commit()
            logger.info(f"Estoque atualizado: ID {id}")
            return True
        except Exception as e:
            logger.error(f"Erro ao atualizar estoque {id}: {e}")
            return False

    def relatorio_estoque(self):
        """Retorna relatório de estoque"""
        try:
            self.cursor.execute("SELECT item, quantidade, valor FROM estoque ORDER BY item")
            return self.cursor.fetchall()
        except Exception as e:
            logger.error(f"Erro ao gerar relatório de estoque: {e}")
            return []
    
    def obter_estoque_critico(self, limite=10):
        """Retorna produtos com estoque crítico"""
        try:
            self.cursor.execute(
                "SELECT id, codigo, item, quantidade, valor FROM estoque WHERE quantidade < ? ORDER BY quantidade",
                (limite,)
            )
            return self.cursor.fetchall()
        except Exception as e:
            logger.error(f"Erro ao obter estoque crítico: {e}")
            return []

    #EXCLUIR ESTOQUE
    def excluir_estoque(self, id):
        """Remove um item do estoque"""
        try:
            self.cursor.execute("DELETE FROM estoque WHERE id = ?", (id,))
            self.conexao.commit()
            logger.info(f"Item removido do estoque: ID {id}")
            return True
        except Exception as e:
            logger.error(f"Erro ao excluir estoque {id}: {e}")
            return False
        
    def cad_estabelecimento(self, nome, CNPJ, telefone, IE, endereco):
        """Cadastra ou atualiza dados do estabelecimento"""
        try:
            # Verificar se existe registro
            self.cursor.execute("SELECT id FROM estabelecimento WHERE id = 1")
            if self.cursor.fetchone():
                self.cursor.execute("""
                    UPDATE estabelecimento
                    SET nome = ?, CNPJ = ?, telefone = ?, IE = ?, endereco = ?
                    WHERE id = 1
                """, (nome, CNPJ, telefone, IE, endereco))
            else:
                self.cursor.execute("""
                    INSERT INTO estabelecimento (id, nome, CNPJ, telefone, IE, endereco)
                    VALUES (1, ?, ?, ?, ?, ?)
                """, (nome, CNPJ, telefone, IE, endereco))
            
            self.conexao.commit()
            logger.info(f"Estabelecimento salvo: {nome}")
            return True
        except Exception as e:
            logger.error(f"Erro ao cadastrar estabelecimento: {e}")
            return False

    def listar_estabelecimento(self):
        """Retorna dados do estabelecimento"""
        try:
            self.cursor.execute("SELECT * FROM estabelecimento WHERE id = 1")
            return self.cursor.fetchone()
        except Exception as e:
            logger.error(f"Erro ao listar estabelecimento: {e}")
            return None
    #  RELATORIO VENDAS PARA RELATORIO DE VENDAS
    def relatorio_vendas(self, ano):
        self.cursor.execute("""SELECT 
        *,
        CASE strftime('%m', data_cadastro)
            WHEN '01' THEN 'Janeiro'
            WHEN '02' THEN 'Fevereiro'
            WHEN '03' THEN 'Março'
            WHEN '04' THEN 'Abril'
            WHEN '05' THEN 'Maio'
            WHEN '06' THEN 'Junho'
            WHEN '07' THEN 'Julho'
            WHEN '08' THEN 'Agosto'
            WHEN '09' THEN 'Setembro'
            WHEN '10' THEN 'Outubro'
            WHEN '11' THEN 'Novembro'
            WHEN '12' THEN 'Dezembro'
        END || '/' || strftime('%Y', data_cadastro) AS mes
    FROM vendas 
    WHERE strftime('%Y', data_cadastro) = ?""", (str(ano),)
    )
        return self.cursor.fetchall()


    def fechar_conexao(self):
        self.conexao.close()
        