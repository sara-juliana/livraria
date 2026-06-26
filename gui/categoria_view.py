import tkinter as tk
from tkinter import ttk, messagebox

from dao.categoria_dao import CategoriaDAO
from models.categoria import Categoria


class CategoriaView:

    def __init__(self, root, voltar):
        self.root = root
        self.dao = CategoriaDAO()
        self.voltar = voltar

        self.tela()

    # =========================
    # TELA PRINCIPAL
    # =========================
    def tela(self):
        self.limpar()

        tk.Label(
            self.root,
            text="📚 Categorias",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        frame = tk.Frame(self.root)
        frame.pack()

        self.tree = ttk.Treeview(
            frame,
            columns=("codigo", "descricao", "qtd"),
            show="headings"
        )

        self.tree.heading("codigo", text="Código")
        self.tree.heading("descricao", text="Descrição")
        self.tree.heading("qtd", text="Qtd Livros")

        self.tree.column("codigo", width=100)
        self.tree.column("descricao", width=250)
        self.tree.column("qtd", width=120, anchor="center")

        self.tree.pack()

        # =========================
        # BOTÕES
        # =========================
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Atualizar", width=12, command=self.carregar).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Adicionar", width=12, command=self.adicionar).grid(row=0, column=1, padx=5)  # 🔥 NOVO
        tk.Button(btn_frame, text="Editar", width=12, command=self.editar).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Excluir", width=12, command=self.excluir).grid(row=0, column=3, padx=5)
        tk.Button(btn_frame, text="Voltar", width=12, command=self.voltar).grid(row=0, column=4, padx=5)

        self.carregar()

    # =========================
    # CARREGAR
    # =========================
    def carregar(self):
        self.tree.delete(*self.tree.get_children())

        for c in self.dao.listar():
            qtd = self.dao.contar_livros(c.codigo)  # 🔥 NOVO

            self.tree.insert(
                "",
                "end",
                values=(c.codigo, c.descricao, qtd)
            )

    # =========================
    # ADICIONAR (NOVO)
    # =========================
    def adicionar(self):
        win = tk.Toplevel(self.root)
        win.title("Nova Categoria")

        tk.Label(win, text="Descrição").grid(row=0, column=0)

        entry = tk.Entry(win)
        entry.grid(row=0, column=1)

        def salvar():
            descricao = entry.get()

            if not descricao:
                messagebox.showerror("Erro", "Descrição obrigatória")
                return

            categoria = Categoria(None, descricao)
            self.dao.salvar(categoria)

            win.destroy()
            self.carregar()

        tk.Button(win, text="Salvar", command=salvar).grid(row=1, column=0, columnspan=2)

    # =========================
    # EDITAR
    # =========================
    def editar(self):
        item = self.tree.focus()

        if not item:
            messagebox.showwarning("Aviso", "Selecione uma categoria")
            return

        values = self.tree.item(item, "values")

        codigo = values[0]
        descricao = values[1]

        win = tk.Toplevel(self.root)
        win.title("Editar Categoria")

        tk.Label(win, text="Código").grid(row=0, column=0)
        tk.Label(win, text=codigo).grid(row=0, column=1)

        tk.Label(win, text="Descrição").grid(row=1, column=0)

        entry = tk.Entry(win)
        entry.insert(0, descricao)
        entry.grid(row=1, column=1)

        def salvar():
            if not entry.get().strip():
                messagebox.showerror("Erro", "Campo obrigatório")
                return

            self.dao.atualizar(codigo, entry.get())
            win.destroy()
            self.carregar()

        tk.Button(win, text="Salvar", command=salvar).grid(row=2, column=0, columnspan=2)
    # =========================
    # EXCLUIR
    # =========================
    def excluir(self):
        item = self.tree.focus()

        if not item:
            messagebox.showwarning("Aviso", "Selecione uma categoria")
            return

        codigo = self.tree.item(item, "values")[0]

        if messagebox.askyesno("Confirmação", "Deseja excluir?"):
            self.dao.excluir(codigo)
            self.carregar()
            
            
    # =========================
    # LIMPAR
    # =========================
    def limpar(self):
        for w in self.root.winfo_children():
            w.destroy()