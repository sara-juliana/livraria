import tkinter as tk
from tkinter import ttk, messagebox

from dao.autor_dao import AutorDAO
from dao.nacionalidade_dao import NacionalidadeDAO
from models.autor import Autor


class AutorView:

    def __init__(self, root, voltar):
        self.root = root
        self.dao = AutorDAO()
        self.nacionalidade_dao = NacionalidadeDAO()
        self.voltar = voltar

        self.tela()

    # =========================
    # TELA PRINCIPAL
    # =========================
    def tela(self):
        self.limpar()

        tk.Label(
            self.root,
            text="👤 Autores",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        frame = tk.Frame(self.root)
        frame.pack()

        self.tree = ttk.Treeview(
            frame,
            columns=("passaporte", "nome", "nacionalidade", "livros"),
            show="headings"
        )

        self.tree.heading("passaporte", text="Passaporte")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("nacionalidade", text="Nacionalidade")
        self.tree.heading("livros", text="Qtd Livros")

        self.tree.column("passaporte", width=120)
        self.tree.column("nome", width=180)
        self.tree.column("nacionalidade", width=150)
        self.tree.column("livros", width=100)

        self.tree.pack()

        # =========================
        # BOTÕES
        # =========================
        btn = tk.Frame(self.root)
        btn.pack(pady=10)

        tk.Button(btn, text="Atualizar", width=12, command=self.carregar).grid(row=0, column=0, padx=5)
        tk.Button(btn, text="Adicionar", width=12, command=self.adicionar).grid(row=0, column=1, padx=5)
        tk.Button(btn, text="Editar", width=12, command=self.editar).grid(row=0, column=2, padx=5)
        tk.Button(btn, text="Excluir", width=12, command=self.excluir).grid(row=0, column=3, padx=5)
        tk.Button(btn, text="Voltar", width=12, command=self.voltar).grid(row=0, column=4, padx=5)

        self.carregar()

    # =========================
    # CARREGAR
    # =========================
    def carregar(self):
        self.tree.delete(*self.tree.get_children())

        autores = self.dao.listar()

        for a in autores:
            qtd = self.dao.contar_livros(a.passaporte)

            nat = a.nacionalidade.descricao if a.nacionalidade else "N/A"

            self.tree.insert(
                "",
                "end",
                values=(a.passaporte, a.nome, nat, qtd)
            )

    # =========================
    # ADICIONAR
    # =========================
    def adicionar(self):
        win = tk.Toplevel(self.root)
        win.title("Novo Autor")

        tk.Label(win, text="Passaporte").grid(row=0, column=0)
        passaporte = tk.Entry(win)
        passaporte.grid(row=0, column=1)

        tk.Label(win, text="Nome").grid(row=1, column=0)
        nome = tk.Entry(win)
        nome.grid(row=1, column=1)

        tk.Label(win, text="Nacionalidade").grid(row=2, column=0)

        nats = self.nacionalidade_dao.listar()
        valores = [n.descricao for n in nats]

        nacionalidade_var = tk.StringVar(win)
        nacionalidade_var.set(valores[0] if valores else "")

        drop = ttk.Combobox(win, textvariable=nacionalidade_var, values=valores, state="readonly")
        drop.grid(row=2, column=1)

        def salvar():
            if not passaporte.get() or not nome.get():
                messagebox.showerror("Erro", "Preencha todos os campos")
                return

            # pega objeto nacionalidade correto
            nacionalidade_obj = None
            for n in nats:
                if n.descricao == nacionalidade_var.get():
                    nacionalidade_obj = n
                    break

            autor = Autor(
                passaporte.get(),
                nome.get(),
                nacionalidade_obj
            )

            self.dao.salvar(autor)

            win.destroy()
            self.carregar()

        tk.Button(win, text="Salvar", command=salvar).grid(row=3, column=0, columnspan=2)

    # =========================
    # EDITAR
    # =========================
    def editar(self):
        item = self.tree.focus()

        if not item:
            messagebox.showwarning("Aviso", "Selecione um autor")
            return

        passaporte, nome, _, _ = self.tree.item(item, "values")

        win = tk.Toplevel(self.root)
        win.title("Editar Autor")

        tk.Label(win, text="Passaporte").grid(row=0, column=0)
        tk.Label(win, text=passaporte).grid(row=0, column=1)

        tk.Label(win, text="Nome").grid(row=1, column=0)

        nome_entry = tk.Entry(win)
        nome_entry.insert(0, nome)
        nome_entry.grid(row=1, column=1)

        def salvar():
            if not nome_entry.get():
                messagebox.showerror("Erro", "Nome obrigatório")
                return

            self.dao.atualizar(passaporte, nome_entry.get())
            win.destroy()
            self.carregar()

        tk.Button(win, text="Salvar", command=salvar).grid(row=2, column=0, columnspan=2)

    # =========================
    # EXCLUIR
    # =========================
    def excluir(self):
        item = self.tree.focus()

        if not item:
            messagebox.showwarning("Aviso", "Selecione um autor")
            return

        passaporte, _, _, _ = self.tree.item(item, "values")

        if messagebox.askyesno("Confirmação", "Deseja excluir este autor?"):
            self.dao.excluir(passaporte)
            self.carregar()

    # =========================
    # LIMPAR
    # =========================
    def limpar(self):
        for w in self.root.winfo_children():
            w.destroy()
