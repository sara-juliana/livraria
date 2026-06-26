from database.db import conectar
from models.autor import Autor
from models.nacionalidade import Nacionalidade


class AutorDAO:

    def salvar(self, autor: Autor):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO autor (passaporte, nome, nacionalidade_codigo)
            VALUES (?, ?, ?)
        """, (
            autor.passaporte,
            autor.nome,
            autor.nacionalidade.codigo if autor.nacionalidade else None
        ))

        conn.commit()
        conn.close()

    def listar(self):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT a.passaporte, a.nome, n.codigo, n.descricao
            FROM autor a
            LEFT JOIN nacionalidade n
            ON a.nacionalidade_codigo = n.codigo
        """)

        rows = cursor.fetchall()
        conn.close()

        autores = []

        for passaporte, nome, codigo, descricao in rows:
            nacionalidade = Nacionalidade(codigo, descricao) if codigo else None
            autores.append(Autor(passaporte, nome, nacionalidade))

        return autores

    def contar(self):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM autor")

        qtd = cursor.fetchone()[0]
        conn.close()

        return qtd

    def excluir(self, passaporte):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM autor
            WHERE passaporte = ?
        """, (passaporte,))

        conn.commit()
        conn.close()
        
    def atualizar(self, passaporte, nome):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE autor
            SET nome = ?
            WHERE passaporte = ?
        """, (nome, passaporte))

        conn.commit()
        conn.close()
        
    def contar_por_nacionalidade(self, codigo_nacionalidade):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM autor
            WHERE nacionalidade_codigo = ?
        """, (codigo_nacionalidade,))

        qtd = cursor.fetchone()[0]
        conn.close()

        return qtd

    def contar_livros(self, passaporte):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM livro_autor
            WHERE passaporte = ?
        """, (passaporte,))

        qtd = cursor.fetchone()[0]
        conn.close()

        return qtd
