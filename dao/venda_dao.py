from database.db import conectar


class VendaDAO:

    def vender(self, isbn, quantidade):
        conn = conectar()
        cursor = conn.cursor()

        try:
            if quantidade <= 0:
                raise ValueError("A quantidade deve ser maior que zero.")

            cursor.execute("""
                SELECT titulo, quantidade_exemplares, preco, tipo
                FROM livro
                WHERE isbn = ?
            """, (isbn,))

            livro = cursor.fetchone()

            if not livro:
                raise ValueError("Livro não encontrado.")

            titulo, estoque, preco, tipo = livro

            # Livro físico precisa controlar estoque
            if quantidade > estoque:
                raise ValueError(
                    f"Estoque insuficiente. Estoque atual: {estoque}"
                )

            novo_estoque = estoque - quantidade

            cursor.execute("""
                UPDATE livro
                SET quantidade_exemplares = ?
                WHERE isbn = ?
            """, (novo_estoque, isbn))

            # Livro digital não reduz estoque
            valor_total = quantidade * preco

            cursor.execute("""
                INSERT INTO venda (
                    isbn, quantidade, valor_unitario, valor_total
                )
                VALUES (?, ?, ?, ?)
            """, (
                isbn,
                quantidade,
                preco,
                valor_total
            ))

            conn.commit()

            return {
                "titulo": titulo,
                "tipo": tipo,
                "quantidade": quantidade,
                "valor_unitario": preco,
                "valor_total": valor_total
            }

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            conn.close()

    def total_caixa(self):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COALESCE(SUM(valor_total), 0)
            FROM venda
        """)

        total = cursor.fetchone()[0]

        conn.close()
        return total

    def total_vendas(self):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COALESCE(COUNT(*), 0)
            FROM venda
        """)

        total = cursor.fetchone()[0]

        conn.close()
        return total

    def listar_vendas(self):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                v.codigo,
                l.titulo,
                l.tipo,
                v.quantidade,
                v.valor_unitario,
                v.valor_total,
                v.data_venda
            FROM venda v
            INNER JOIN livro l ON l.isbn = v.isbn
            ORDER BY v.codigo DESC
        """)

        vendas = cursor.fetchall()

        conn.close()
        return vendas
