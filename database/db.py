import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parents[2] / "biblioteca.db"


# =========================
# CONEXÃO
# =========================
def conectar():
    conn = sqlite3.connect(DB_PATH)

    # 🔥 garante integridade relacional no SQLite
    conn.execute("PRAGMA foreign_keys = ON")

    return conn


# =========================
# CRIAÇÃO DE TABELAS
# =========================
def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()

    # =========================
    # EDITORA
    # =========================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS editora (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cnpj TEXT NOT NULL UNIQUE,
            razao_social TEXT NOT NULL
        )
    """)

    # =========================
    # CATEGORIA
    # =========================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categoria (
            codigo INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL UNIQUE
        )
    """)

    # =========================
    # NACIONALIDADE
    # =========================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nacionalidade (
            codigo INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL UNIQUE
        )
    """)

    # =========================
    # AUTOR
    # =========================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS autor (
            passaporte TEXT PRIMARY KEY,
            nome TEXT NOT NULL,
            nacionalidade_codigo INTEGER,

            FOREIGN KEY (nacionalidade_codigo)
                REFERENCES nacionalidade(codigo)
                ON DELETE SET NULL
        )
    """)

    # =========================
    # LIVRO (BASE)
    # =========================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS livro (
            isbn TEXT PRIMARY KEY,
            titulo TEXT NOT NULL,
            ano INTEGER NOT NULL,

            editora_id INTEGER,
            categoria_codigo INTEGER,

            quantidade_exemplares INTEGER NOT NULL,
            preco REAL NOT NULL,

            tipo TEXT NOT NULL, -- FISICO | DIGITAL

            FOREIGN KEY (editora_id)
                REFERENCES editora(id)
                ON DELETE SET NULL,

            FOREIGN KEY (categoria_codigo)
                REFERENCES categoria(codigo)
                ON DELETE SET NULL
        )
    """)

    # =========================
    # LIVRO FÍSICO
    # =========================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS livro_fisico (
            isbn TEXT PRIMARY KEY,

            paginas INTEGER,
            peso REAL,
            altura REAL,
            largura REAL,
            profundidade REAL,
            localizacao_estante TEXT,

            FOREIGN KEY (isbn)
                REFERENCES livro(isbn)
                ON DELETE CASCADE
        )
    """)

    # =========================
    # LIVRO DIGITAL
    # =========================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS livro_digital (
            isbn TEXT PRIMARY KEY,

            formato TEXT,
            tamanho_mb REAL,
            link_download TEXT,
            possui_drm INTEGER DEFAULT 0,

            FOREIGN KEY (isbn)
                REFERENCES livro(isbn)
                ON DELETE CASCADE
        )
    """)

    # =========================
    # RELAÇÃO LIVRO - AUTOR (N:N)
    # =========================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS livro_autor (
            isbn TEXT NOT NULL,
            passaporte TEXT NOT NULL,

            PRIMARY KEY (isbn, passaporte),

            FOREIGN KEY (isbn)
                REFERENCES livro(isbn)
                ON DELETE CASCADE,

            FOREIGN KEY (passaporte)
                REFERENCES autor(passaporte)
                ON DELETE CASCADE
        )
    """)

    # =========================
    # RELAÇÃO LIVRO - EDITORA (ERP LIMPO)
    # =========================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS editora_livro (
            editora_id INTEGER NOT NULL,
            isbn TEXT NOT NULL,

            PRIMARY KEY (editora_id, isbn),

            FOREIGN KEY (editora_id)
                REFERENCES editora(id)
                ON DELETE CASCADE,

            FOREIGN KEY (isbn)
                REFERENCES livro(isbn)
                ON DELETE CASCADE
        )
    """)



    # =========================
    # VENDA / CAIXA
    # =========================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS venda (
            codigo INTEGER PRIMARY KEY AUTOINCREMENT,
            isbn TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            valor_unitario REAL NOT NULL,
            valor_total REAL NOT NULL,
            data_venda TEXT DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (isbn)
                REFERENCES livro(isbn)
                ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()
