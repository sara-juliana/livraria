from database.db import conectar
from models.nacionalidade import Nacionalidade


class NacionalidadeDAO:

    def salvar(self, nacionalidade: Nacionalidade):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO nacionalidade (descricao)
            VALUES (?)
        """, (nacionalidade.descricao,))

        conn.commit()
        conn.close()

    def listar(self):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT codigo, descricao FROM nacionalidade")
        rows = cursor.fetchall()

        conn.close()

        return [Nacionalidade(codigo, descricao) for codigo, descricao in rows]

    def contar(self):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM nacionalidade")

        qtd = cursor.fetchone()[0]
        conn.close()

        return qtd

    def atualizar(self, codigo, descricao):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE nacionalidade
            SET descricao = ?
            WHERE codigo = ?
        """, (descricao, codigo))

        conn.commit()
        conn.close()

    def excluir(self, codigo):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM nacionalidade
            WHERE codigo = ?
        """, (codigo,))

        conn.commit()
        conn.close()
