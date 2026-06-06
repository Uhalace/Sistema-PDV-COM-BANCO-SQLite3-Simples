import os
import sqlite3

class Banco:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.abspath(os.path.join(base_dir, '..', 'Banco', 'base.db'))
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        self.conexao = sqlite3.connect(db_path)
        self.cursor = self.conexao.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_nota INTEGER NOT NULL,
                item TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                valor INTEGER NOT NULL,
                subtotal INTEGER NOT NULL
            )
        """)
        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS estoque (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    codigo INTEGER NOT NULL,
                    item VARCHAR(250) NOT NULL,
                     quantidade INTEGER NOT NULL,
                    valor INTEGER NOT NULL)
                """)

        self.conexao.commit()

    def inserir_venda(self, numero_nota, item, quantidade, valor, subtotal):
        self.cursor.execute("""
            INSERT INTO vendas (numero_nota, item, quantidade, valor, subtotal)
            VALUES (?, ?, ?, ?, ?)
        """, (numero_nota, item, quantidade, valor, subtotal))
        self.conexao.commit()

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

    def Bucar_item(self, codigo):
        self.cursor.execute("SELECT * FROM estoque WHERE codigo = ?", (codigo,))
        return self.cursor.fetchone()
        

    def fechar_conexao(self):
        self.conexao.close()
        