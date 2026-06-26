from database.db import conectar
from models.editora import Editora


class EditoraDAO:

    # =========================
    # SALVAR
    # =========================
    def salvar(self, editora: Editora):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO editora (cnpj, razao_social)
            VALUES (?, ?)
        """, (editora.cnpj, editora.razao_social))

        conn.commit()
        conn.close()

    # =========================
    # LISTAR (OBJETOS)
    # =========================
    def listar(self):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT cnpj, razao_social FROM editora")
        rows = cursor.fetchall()

        conn.close()

        return [Editora(cnpj, razao) for cnpj, razao in rows]

    # =========================
    # ATUALIZAR
    # =========================
    def atualizar(self, cnpj, nova_razao):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE editora
            SET razao_social = ?
            WHERE cnpj = ?
        """, (nova_razao, cnpj))

        conn.commit()
        conn.close()

    # =========================
    # EXCLUIR
    # =========================
    def excluir(self, cnpj):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM editora
            WHERE cnpj = ?
        """, (cnpj,))

        conn.commit()
        conn.close()
        
        
    def buscar_id_por_cnpj(self, cnpj):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id FROM editora WHERE cnpj = ?
        """, (cnpj,))

        row = cursor.fetchone()
        conn.close()

        return row[0] if row else None        
        
        
    def contar_livros(self, cnpj):
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