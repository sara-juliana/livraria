import sqlite3

from dao.livro_dao import LivroDAO
import dao.livro_dao as livro_dao_module


def test_contar_exemplares_por_tipo_soma_quantidade(tmp_path, monkeypatch):
    db_path = tmp_path / "test_biblioteca.db"
    conn = sqlite3.connect(db_path)

    conn.execute("""
        CREATE TABLE livro (
            isbn TEXT PRIMARY KEY,
            titulo TEXT NOT NULL,
            ano INTEGER NOT NULL,
            editora_id INTEGER,
            categoria_codigo INTEGER,
            quantidade_exemplares INTEGER NOT NULL,
            preco REAL NOT NULL,
            tipo TEXT NOT NULL
        )
    """)

    conn.execute(
        "INSERT INTO livro VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        ("1", "Livro 1", 2024, None, None, 3, 10.0, "FISICO"),
    )
    conn.execute(
        "INSERT INTO livro VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        ("2", "Livro 2", 2024, None, None, 5, 20.0, "FISICO"),
    )
    conn.execute(
        "INSERT INTO livro VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        ("3", "Livro 3", 2024, None, None, 2, 15.0, "DIGITAL"),
    )
    conn.commit()
    conn.close()

    monkeypatch.setattr(livro_dao_module, "conectar", lambda: sqlite3.connect(db_path))

    dao = LivroDAO()

    assert dao.contar_exemplares_por_tipo("FISICO") == 8
    assert dao.contar_exemplares_por_tipo("DIGITAL") == 2
