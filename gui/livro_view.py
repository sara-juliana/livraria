import tkinter as tk
from tkinter import ttk, messagebox

from dao.livro_dao import LivroDAO


class LivroView:

    def __init__(self, root, voltar):
        self.root = root
        self.dao = LivroDAO()
        self.voltar = voltar

        self.tela()

    # =========================
    # TELA PRINCIPAL
    # =========================
    def tela(self):
        self.limpar()

        tk.Label(
            self.root,
            text="📘 Biblioteca de Livros",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        # ================= TREEVIEW =================
        frame = tk.Frame(self.root)
        frame.pack()

        self.tree = ttk.Treeview(
            frame,
            columns=(
                "isbn", "titulo", "ano",
                "editora", "categoria",
                "tipo", "qtd", "preco", "total"
            ),
            show="headings"
        )

        self.tree.heading("isbn", text="ISBN")
        self.tree.heading("titulo", text="Título")
        self.tree.heading("ano", text="Ano")
        self.tree.heading("editora", text="Editora")
        self.tree.heading("categoria", text="Categoria")
        self.tree.heading("tipo", text="Tipo")
        self.tree.heading("qtd", text="Qtd")
        self.tree.heading("preco", text="Preço")
        self.tree.heading("total", text="Total")

        self.tree.pack(fill="both", expand=True)

        # ================= BOTÕES =================
        btn = tk.Frame(self.root)
        btn.pack(pady=10)

        tk.Button(btn, text="🔄 Atualizar", width=15, command=self.carregar).grid(row=0, column=0, padx=5)
        tk.Button(btn, text="📖 Livro Físico", width=15, command=self.abrir_fisico).grid(row=0, column=1, padx=5)
        tk.Button(btn, text="💻 Livro Digital", width=15, command=self.abrir_digital).grid(row=0, column=2, padx=5)
        tk.Button(btn, text="🗑 Excluir", width=15, command=self.excluir).grid(row=0, column=3, padx=5)
        tk.Button(btn, text="🔙 Voltar", width=15, command=self.voltar).grid(row=0, column=4, padx=5)

        self.carregar()

    # =========================
    # CARREGAR DADOS COMPLETOS
    # =========================
    def carregar(self):
        self.tree.delete(*self.tree.get_children())

        livros = self.dao.listar_completo()  # 🔥 precisa JOIN no DAO

        for l in livros:

            tipo = "Físico" if l.get("tipo") == "F" else "Digital"

            self.tree.insert(
                "",
                "end",
                values=(
                    l["isbn"],
                    l["titulo"],
                    l["ano"],
                    l["editora"],
                    l["categoria"],
                    tipo,
                    l["qtd"],
                    f"R$ {l['preco']:.2f}",
                    f"R$ {l['total']:.2f}"
                )
            )

    # =========================
    # ABRIR CADASTRO FÍSICO
    # =========================
    def abrir_fisico(self):
        from gui.livro_fisico_view import LivroFisicoView
        LivroFisicoView(self.root, self.tela)

    # =========================
    # ABRIR CADASTRO DIGITAL
    # =========================
    def abrir_digital(self):
        from gui.livro_digital_view import LivroDigitalView
        LivroDigitalView(self.root, self.tela)

    # =========================
    # EXCLUIR
    # =========================
    def excluir(self):
        item = self.tree.focus()

        if not item:
            messagebox.showwarning("Aviso", "Selecione um livro")
            return

        isbn = self.tree.item(item, "values")[0]

        if messagebox.askyesno("Confirmação", "Deseja excluir este livro?"):
            self.dao.excluir(isbn)
            self.carregar()

    # =========================
    # LIMPAR
    # =========================
    def limpar(self):
        for w in self.root.winfo_children():
            w.destroy()