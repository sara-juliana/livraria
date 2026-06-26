from database.db import conectar


class LivroAutorDAO:

    def vincular(self, isbn, passaporte):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO livro_autor (isbn, passaporte)
            VALUES (?, ?)
        """, (isbn, passaporte))

        conn.commit()
        conn.close()

    def listar_autores_do_livro(self, isbn):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT a.passaporte, a.nome
            FROM autor a
            INNER JOIN livro_autor la
            ON a.passaporte = la.passaporte
            WHERE la.isbn = ?
        """, (isbn,))

        rows = cursor.fetchall()
        conn.close()

        return rows

    def remover_vinculo(self, isbn, passaporte):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM livro_autor
            WHERE isbn = ? AND passaporte = ?
        """, (isbn, passaporte))

        conn.commit()
        conn.close()