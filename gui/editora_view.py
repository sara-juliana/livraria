import tkinter as tk
from tkinter import ttk, messagebox

from dao.editora_dao import EditoraDAO
from dao.livro_dao import LivroDAO
from models.editora import Editora


class EditoraView:

    def __init__(self, root, voltar_menu):
        self.root = root
        self.dao = EditoraDAO()
        self.livro_dao = LivroDAO()
        self.voltar_menu = voltar_menu

        self.tela()

    # =========================
    # TELA
    # =========================
    def tela(self):
        self.limpar()

        tk.Label(
            self.root,
            text="📚 Editoras",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        frame = tk.Frame(self.root)
        frame.pack()

        self.tree = ttk.Treeview(
            frame,
            columns=("cnpj", "razao", "qtd"),
            show="headings"
        )

        self.tree.heading("cnpj", text="CNPJ")
        self.tree.heading("razao", text="Razão Social")
        self.tree.heading("qtd", text="Qtd Livros")

        self.tree.column("cnpj", width=150)
        self.tree.column("razao", width=250)
        self.tree.column("qtd", width=120, anchor="center")

        self.tree.pack()

        # =========================
        # BOTÕES
        # =========================
        btn = tk.Frame(self.root)
        btn.pack(pady=10)

        tk.Button(btn, text="Atualizar", command=self.carregar).grid(row=0, column=0, padx=5)
        tk.Button(btn, text="Adicionar", command=self.adicionar).grid(row=0, column=1, padx=5)
        tk.Button(btn, text="Editar", command=self.editar).grid(row=0, column=2, padx=5)
        tk.Button(btn, text="Excluir", command=self.excluir).grid(row=0, column=3, padx=5)
        tk.Button(btn, text="Voltar", command=self.voltar_menu).grid(row=0, column=4, padx=5)

        self.carregar()

    # =========================
    # CARREGAR
    # =========================
    def carregar(self):
        self.tree.delete(*self.tree.get_children())

        editoras = self.dao.listar()

        for e in editoras:

            # ✔ conta livros corretamente (ERP consistente)
            qtd = self.livro_dao.contar_por_editora(e.cnpj)

            self.tree.insert(
                "",
                "end",
                values=(e.cnpj, e.razao_social, qtd)
            )

    # =========================
    # ADICIONAR
    # =========================
    def adicionar(self):
        win = tk.Toplevel(self.root)
        win.title("Nova Editora")

        tk.Label(win, text="CNPJ").grid(row=0, column=0)
        cnpj = tk.Entry(win)
        cnpj.grid(row=0, column=1)

        tk.Label(win, text="Razão Social").grid(row=1, column=0)
        razao = tk.Entry(win)
        razao.grid(row=1, column=1)

        def salvar():
            if not cnpj.get() or not razao.get():
                messagebox.showerror("Erro", "Preencha todos os campos")
                return

            editora = Editora(cnpj.get(), razao.get())
            self.dao.salvar(editora)

            win.destroy()
            self.carregar()

        tk.Button(win, text="Salvar", command=salvar).grid(row=2, column=0, columnspan=2)

    # =========================
    # EDITAR (CORRIGIDO)
    # =========================
    def editar(self):
        item = self.tree.focus()

        if not item:
            messagebox.showwarning("Aviso", "Selecione uma editora")
            return

        cnpj, razao, _ = self.tree.item(item, "values")

        win = tk.Toplevel(self.root)
        win.title("Editar Editora")

        tk.Label(win, text="CNPJ").grid(row=0, column=0)
        tk.Label(win, text=cnpj).grid(row=0, column=1)

        tk.Label(win, text="Razão Social").grid(row=1, column=0)

        razao_entry = tk.Entry(win)
        razao_entry.insert(0, razao)
        razao_entry.grid(row=1, column=1)

        def salvar():
            if not razao_entry.get():
                messagebox.showerror("Erro", "Campo obrigatório")
                return

            self.dao.atualizar(cnpj, razao_entry.get())

            win.destroy()
            self.carregar()

        tk.Button(win, text="Salvar", command=salvar).grid(row=2, column=0, columnspan=2)

    # =========================
    # EXCLUIR
    # =========================
    def excluir(self):
        item = self.tree.focus()

        if not item:
            messagebox.showwarning("Aviso", "Selecione uma editora")
            return

        cnpj = self.tree.item(item, "values")[0]

        if messagebox.askyesno("Confirmação", "Deseja excluir?"):
            self.dao.excluir(cnpj)
            self.carregar()

    # =========================
    # LIMPAR
    # =========================
    def limpar(self):
        for w in self.root.winfo_children():
            w.destroy()