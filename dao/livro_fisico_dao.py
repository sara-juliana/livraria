from database.db import conectar
from dao.editora_dao import EditoraDAO




class LivroFisicoDAO:

    # =========================
    # SALVAR
    # =========================
    def salvar(self, livro):

        conn = conectar()
        cursor = conn.cursor()

        # resolve FK editora (CNPJ -> ID)
        editora_id = EditoraDAO().buscar_id_por_cnpj(livro.editora.cnpj)

        if not editora_id:
            raise ValueError("Editora inválida")

        # ================= LIVRO BASE =================
        cursor.execute("""
            INSERT INTO livro (
                isbn, titulo, ano,
                editora_id, categoria_codigo,
                quantidade_exemplares, preco, tipo
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, 'FISICO')
        """, (
            livro.isbn,
            livro.titulo,
            livro.ano,
            editora_id,
            livro.categoria.codigo,
            livro.quantidade_exemplares,
            livro.preco
        ))

        # ================= LIVRO FÍSICO =================
        cursor.execute("""
            INSERT INTO livro_fisico (
                isbn, paginas, peso,
                altura, largura, profundidade,
                localizacao_estante
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            livro.isbn,
            livro.paginas,
            livro.peso,
            livro.altura,
            livro.largura,
            livro.profundidade,
            livro.localizacao_estante
        ))

        # ================= AUTORES =================
        for autor in livro.autores:
            cursor.execute("""
                INSERT INTO livro_autor (isbn, passaporte)
                VALUES (?, ?)
            """, (livro.isbn, autor.passaporte))

        conn.commit()
        conn.close()

    # =========================
    # LISTAR COMPLETO
    # =========================
    def listar(self):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                l.isbn,
                l.titulo,
                l.ano,
                l.quantidade_exemplares,
                l.preco,

                e.razao_social,
                c.descricao,

                lf.paginas,
                lf.peso,
                lf.altura,
                lf.largura,
                lf.profundidade,
                lf.localizacao_estante,

                GROUP_CONCAT(a.nome, ', ') as autores

            FROM livro l

            LEFT JOIN editora e ON e.id = l.editora_id
            LEFT JOIN categoria c ON c.codigo = l.categoria_codigo
            LEFT JOIN livro_fisico lf ON lf.isbn = l.isbn
            LEFT JOIN livro_autor la ON la.isbn = l.isbn
            LEFT JOIN autor a ON a.passaporte = la.passaporte

            WHERE l.tipo = 'FISICO'

            GROUP BY l.isbn
        """)

        rows = cursor.fetchall()
        conn.close()

        return rows

    # =========================
    # EXCLUIR
    # =========================
    def excluir(self, isbn):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM livro WHERE isbn = ?", (isbn,))

        conn.commit()
        conn.close()

    # =========================
    # ATUALIZAR
    # =========================
    def atualizar(self, isbn, titulo):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE livro
            SET titulo = ?
            WHERE isbn = ?
        """, (titulo, isbn))

        conn.commit()
        conn.close()
        
    def atualizar_qtd_preco(self, isbn, quantidade, preco):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE livro
            SET quantidade_exemplares = ?, preco = ?
            WHERE isbn = ?
        """, (quantidade, preco, isbn))

        conn.commit()
        conn.close()
        
        
