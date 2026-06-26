import sqlite3

import pytest

import dao.livro_dao as livro_dao_module
import dao.venda_dao as venda_dao_module
from dao.livro_dao import LivroDAO
from dao.venda_dao import VendaDAO


@pytest.fixture
def banco_temporario(tmp_path, monkeypatch):
    db_path = tmp_path / "biblioteca_test.db"
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

    conn.execute("""
        CREATE TABLE venda (
            codigo INTEGER PRIMARY KEY AUTOINCREMENT,
            isbn TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            valor_unitario REAL NOT NULL,
            valor_total REAL NOT NULL,
            data_venda TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.execute(
        "INSERT INTO livro VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        ("1", "Livro A", 2024, None, None, 5, 10.0, "FISICO"),
    )
    conn.execute(
        "INSERT INTO livro VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        ("2", "Livro B", 2024, None, None, 2, 20.0, "DIGITAL"),
    )
    conn.commit()
    conn.close()

    monkeypatch.setattr(livro_dao_module, "conectar", lambda: sqlite3.connect(db_path))
    monkeypatch.setattr(venda_dao_module, "conectar", lambda: sqlite3.connect(db_path))

    return db_path


def test_contar_exemplares_por_tipo_soma_quantidade(banco_temporario):
    dao = LivroDAO()

    assert dao.contar_exemplares_por_tipo("FISICO") == 5
    assert dao.contar_exemplares_por_tipo("DIGITAL") == 2


def test_vender_reduz_estoque_e_registra_venda(banco_temporario):
    dao = VendaDAO()

    venda = dao.vender("1", 2)

    assert venda["quantidade"] == 2
    assert venda["valor_total"] == 20.0

    conn = sqlite3.connect(banco_temporario)
    estoque = conn.execute("SELECT quantidade_exemplares FROM livro WHERE isbn = ?", ("1",)).fetchone()[0]
    vendas = conn.execute("SELECT COUNT(*) FROM venda").fetchone()[0]
    conn.close()

    assert estoque == 3
    assert vendas == 1


def test_total_caixa_e_total_vendas(banco_temporario):
    dao = VendaDAO()

    dao.vender("1", 1)
    dao.vender("2", 1)

    assert dao.total_vendas() == 2
    assert dao.total_caixa() == 30.0
