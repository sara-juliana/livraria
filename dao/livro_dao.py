from database.db import conectar
from models.livro import Livro
from dao.editora_dao import EditoraDAO


class LivroDAO:

    # =========================
    # SALVAR LIVRO BASE
    # =========================
    def salvar(self, livro: Livro):
        conn = conectar()
        cursor = conn.cursor()

        # ✔ converte CNPJ -> ID (OBRIGATÓRIO pelo seu banco)
        editora_id = EditoraDAO().buscar_id_por_cnpj(livro.editora.cnpj)

        if not editora_id:
            conn.close()
            raise ValueError("Editora inválida (CNPJ não encontrado)")

        cursor.execute("""
            INSERT INTO livro (
                isbn, titulo, ano,
                editora_id, categoria_codigo,
                quantidade_exemplares, preco, tipo
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, 'BASE')
        """, (
            livro.isbn,
            livro.titulo,
            livro.ano,
            editora_id,
            livro.categoria.codigo,
            livro.quantidade_exemplares,
            livro.preco
        ))

        # =========================
        # RELAÇÃO LIVRO-EDITORA (ERP LIMPO)
        # =========================
        cursor.execute("""
            INSERT INTO editora_livro (editora_id, isbn)
            VALUES (?, ?)
        """, (
            editora_id,
            livro.isbn
        ))

        # =========================
        # RELAÇÃO LIVRO-AUTOR
        # =========================
        for autor in livro.autores:
            cursor.execute("""
                INSERT INTO livro_autor (isbn, passaporte)
                VALUES (?, ?)
            """, (
                livro.isbn,
                autor.passaporte
            ))

        conn.commit()
        conn.close()

    # =========================
    # LISTAR LIVROS (OBJETO)
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
                e.cnpj,
                e.razao_social,
                c.codigo,
                c.descricao
            FROM livro l
            LEFT JOIN editora e ON e.id = l.editora_id
            LEFT JOIN categoria c ON c.codigo = l.categoria_codigo
        """)

        rows = cursor.fetchall()
        conn.close()

        livros = []

        for r in rows:
            livro = Livro(
                r[0],  # isbn
                r[1],  # titulo
                r[2],  # ano
                None,  # editora (pode evoluir depois)
                r[3],  # quantidade
                r[4],  # preco
                None,  # categoria
                []
            )

            livros.append(livro)

        return livros

    # =========================
    # CONTAR EXEMPLARES POR TIPO
    # =========================
    def contar_exemplares_por_tipo(self, tipo):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COALESCE(SUM(quantidade_exemplares), 0)
            FROM livro
            WHERE tipo = ?
        """, (tipo,))

        total = cursor.fetchone()[0] or 0
        conn.close()
        return int(total)

    # =========================
    # LISTAR FÍSICOS
    # =========================
    def listar_fisicos(self):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                l.isbn,
                l.titulo,
                lf.paginas,
                lf.peso,
                lf.localizacao_estante
            FROM livro l
            INNER JOIN livro_fisico lf ON lf.isbn = l.isbn
        """)

        rows = cursor.fetchall()
        conn.close()
        return rows

    # =========================
    # LISTAR DIGITAIS
    # =========================
    def listar_digitais(self):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                l.isbn,
                l.titulo,
                ld.formato,
                ld.tamanho_mb
            FROM livro l
            INNER JOIN livro_digital ld ON ld.isbn = l.isbn
        """)

        rows = cursor.fetchall()
        conn.close()
        return rows

    # =========================
    # CONTAGEM POR EDITORA (CORRETO)
    # =========================
    def contar_por_editora(self, cnpj):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM livro l
            INNER JOIN editora e ON e.id = l.editora_id
            WHERE e.cnpj = ?
        """, (cnpj,))

        qtd = cursor.fetchone()[0]
        conn.close()
        return qtd

    # =========================
    # CONTAGEM POR CATEGORIA
    # =========================
    def contar_por_categoria(self, codigo):
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

    # =========================
    # EXCLUIR
    # =========================
    def excluir(self, isbn):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM livro WHERE isbn = ?", (isbn,))

        conn.commit()
        conn.close()
        
    def comprar(self, isbn, quantidade):
        from dao.venda_dao import VendaDAO

        return VendaDAO().vender(isbn, quantidade)

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT quantidade_exemplares, preco, tipo
            FROM livro
            WHERE isbn = ?
        """, (isbn,))

        row = cursor.fetchone()

        if not row:
            conn.close()
            return 0

        estoque, preco, tipo = row

        # regra: digital não controla estoque (opcional ERP real)
        if tipo == "FISICO":
            if quantidade > estoque:
                conn.close()
                raise ValueError("Estoque insuficiente")

            novo_estoque = estoque - quantidade

            cursor.execute("""
                UPDATE livro
                SET quantidade_exemplares = ?
                WHERE isbn = ?
            """, (novo_estoque, isbn))

        total = quantidade * preco

        conn.commit()
        conn.close()

        return total
