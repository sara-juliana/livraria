from database.db import conectar
from models.categoria import Categoria


class CategoriaDAO:

    def salvar(self, categoria: Categoria):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO categoria (descricao)
            VALUES (?)
        """, (categoria.descricao,))

        conn.commit()
        conn.close()

    def listar(self):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT codigo, descricao FROM categoria")
        rows = cursor.fetchall()

        conn.close()

        return [Categoria(codigo, descricao) for codigo, descricao in rows]

    def atualizar(self, codigo, descricao):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE categoria
            SET descricao = ?
            WHERE codigo = ?
        """, (descricao, codigo))

        conn.commit()
        conn.close()

    def excluir(self, codigo):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM categoria
            WHERE codigo = ?
        """, (codigo,))

        conn.commit()
        conn.close()
        
    def contar_livros(self, codigo):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM livro
            WHERE categoria_codigo = ?
        """, (codigo,))

        qtd = cursor.fetchone()[0]
        conn.close()

        return qtd
    
    def listar_com_qtd(self):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT c.codigo, c.descricao, COUNT(l.isbn)
            FROM categoria c
            LEFT JOIN livro l ON l.categoria_codigo = c.codigo
            GROUP BY c.codigo, c.descricao
        """)

        rows = cursor.fetchall()
        conn.close()

        return rows    
    
    
