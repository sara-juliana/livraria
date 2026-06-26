import tkinter as tk
from tkinter import ttk, messagebox

from dao.livro_fisico_dao import LivroFisicoDAO
from dao.categoria_dao import CategoriaDAO
from dao.editora_dao import EditoraDAO
from dao.autor_dao import AutorDAO

from models.livro import LivroFisico


from dao.venda_dao import VendaDAO


class LivroFisicoView:

    def __init__(self, root, voltar, processar_compra=None):
        self.root = root
        self.dao = LivroFisicoDAO()
        self.venda_dao = VendaDAO()
        self.voltar = voltar
        self.processar_compra = processar_compra
        self.tela()

    # =========================
    # DADOS
    # =========================
    def carregar_dados(self):
        self.categorias = CategoriaDAO().listar()
        self.editoras = EditoraDAO().listar()
        self.autores = AutorDAO().listar()

    # =========================
    # TELA
    # =========================
    def tela(self):
        self.limpar()
        self.carregar_dados()

        tk.Label(self.root, text="📖 Livros Físicos", font=("Arial", 14, "bold")).pack(pady=10)

        frame = tk.Frame(self.root)
        frame.pack()

        self.tree = ttk.Treeview(
            frame,
            columns=("isbn", "titulo", "editora", "categoria", "qtd", "preco"),
            show="headings"
        )

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.upper())

        self.tree.pack()

        btn = tk.Frame(self.root)
        btn.pack(pady=10)

        tk.Button(btn, text="Atualizar", command=self.carregar).grid(row=0, column=0)
        tk.Button(btn, text="Novo", command=self.adicionar).grid(row=0, column=1)
        tk.Button(btn, text="Detalhes", command=self.detalhes).grid(row=0, column=2)
        tk.Button(btn, text="Atualizar Livro", command=self.atualizar_livro).grid(row=0, column=3)
        tk.Button(btn, text="Comprar", command=self.comprar).grid(row=0, column=4)
        tk.Button(btn, text="Excluir", command=self.excluir).grid(row=0, column=5)
        tk.Button(btn, text="Voltar", command=self.voltar).grid(row=0, column=6)

        self.carregar()

    # =========================
    # LISTAGEM
    # =========================
    def carregar(self):
        self.carregar_dados()
        self.tree.delete(*self.tree.get_children())

        for l in self.dao.listar():

            # proteção contra estrutura diferente
            isbn = l[0]
            titulo = l[1]
            quantidade = l[3] if len(l) > 3 else 0
            preco = l[4] if len(l) > 4 else 0

            editora = l[5] if len(l) > 5 else ""
            categoria = l[6] if len(l) > 6 else ""

            self.tree.insert("", "end", values=(
                isbn,
                titulo,
                editora,
                categoria,
                quantidade,
                f"R$ {float(preco):.2f}"
            ))

    # =========================
    # DETALHES
    # =========================
    def detalhes(self):
        item = self.tree.focus()

        if not item:
            messagebox.showwarning("Aviso", "Selecione um livro")
            return

        isbn = self.tree.item(item, "values")[0]

        livro = next((l for l in self.dao.listar() if l[0] == isbn), None)

        if not livro:
            return

        win = tk.Toplevel(self.root)
        win.title("Detalhes")

        tk.Label(win, text=f"""
ISBN: {livro[0]}
Título: {livro[1]}
Ano: {livro[2] if len(livro) > 2 else ''}
Editora: {livro[5] if len(livro) > 5 else ''}
Categoria: {livro[6] if len(livro) > 6 else ''}

Quantidade: {livro[3] if len(livro) > 3 else 0}
Preço: R$ {livro[4] if len(livro) > 4 else 0}

Páginas: {livro[7] if len(livro) > 7 else ''}
Peso: {livro[8] if len(livro) > 8 else ''} g
""").pack(padx=10, pady=10)

    # =========================
    # ATUALIZAR PREÇO / QTD
    # =========================
    def atualizar_livro(self):
        item = self.tree.focus()

        if not item:
            messagebox.showwarning("Aviso", "Selecione um livro")
            return

        isbn = self.tree.item(item, "values")[0]

        win = tk.Toplevel(self.root)
        win.title("Atualizar Livro")

        tk.Label(win, text="Quantidade").grid(row=0, column=0)
        qtd = tk.Entry(win)
        qtd.grid(row=0, column=1)

        tk.Label(win, text="Preço").grid(row=1, column=0)
        preco = tk.Entry(win)
        preco.grid(row=1, column=1)

        def salvar():
            try:
                qtd_val = int(qtd.get())
                preco_val = float(preco.get())
            except:
                messagebox.showerror("Erro", "Valores inválidos")
                return

            self.dao.atualizar_qtd_preco(isbn, qtd_val, preco_val)
            win.destroy()
            self.carregar()

        tk.Button(win, text="Salvar", command=salvar).grid(row=2, column=0, columnspan=2)

    # =========================
    # ADICIONAR
    # =========================
    def adicionar(self):
        self.carregar_dados()

        win = tk.Toplevel(self.root)
        win.title("Novo Livro Físico")

        tk.Label(win, text="ISBN").grid(row=0, column=0)
        isbn = tk.Entry(win)
        isbn.grid(row=0, column=1)

        tk.Label(win, text="Título").grid(row=1, column=0)
        titulo = tk.Entry(win)
        titulo.grid(row=1, column=1)

        tk.Label(win, text="Ano").grid(row=2, column=0)
        ano = tk.Entry(win)
        ano.grid(row=2, column=1)

        # categoria
        cat_map = {c.descricao: c for c in self.categorias}
        tk.Label(win, text="Categoria").grid(row=3, column=0)
        cat = ttk.Combobox(win, values=list(cat_map.keys()), state="readonly")
        cat.grid(row=3, column=1)

        # editora
        edi_map = {e.razao_social: e for e in self.editoras}

        tk.Label(win, text="Editora").grid(row=4, column=0)
        edi = ttk.Combobox(win, values=list(edi_map.keys()), state="readonly")
        edi.grid(row=4, column=1)

        # autores
        tk.Label(win, text="Autores").grid(row=5, column=0)
        lb = tk.Listbox(win, selectmode="multiple")
        lb.grid(row=5, column=1)

        for a in self.autores:
            lb.insert(tk.END, a.nome)

        tk.Label(win, text="Qtd").grid(row=6, column=0)
        qtd = tk.Entry(win)
        qtd.grid(row=6, column=1)

        tk.Label(win, text="Preço").grid(row=7, column=0)
        preco = tk.Entry(win)
        preco.grid(row=7, column=1)

        tk.Label(win, text="Páginas").grid(row=8, column=0)
        paginas = tk.Entry(win)
        paginas.grid(row=8, column=1)

        tk.Label(win, text="Peso (g)").grid(row=9, column=0)
        peso = tk.Entry(win)
        peso.grid(row=9, column=1)

        def salvar():

            if not isbn.get() or not titulo.get():
                messagebox.showerror("Erro", "Campos obrigatórios")
                return

            if cat.get() not in cat_map or edi.get() not in edi_map:
                messagebox.showerror("Erro", "Selecione categoria e editora")
                return

            livro = LivroFisico(
                isbn.get(),
                titulo.get(),
                int(ano.get() or 2024),
                edi_map[edi.get()],
                int(qtd.get() or 1),
                float(preco.get() or 0),
                cat_map[cat.get()],
                [self.autores[i] for i in lb.curselection()],
                int(paginas.get() or 0),
                float(peso.get() or 0),
                0, 0, 0,
                "A1"
            )

            self.dao.salvar(livro)
            win.destroy()
            self.carregar()

        tk.Button(win, text="Salvar", command=salvar).grid(row=10, column=0, columnspan=2)


    def comprar(self):
        item = self.tree.focus()

        if not item:
            messagebox.showwarning("Aviso", "Selecione um livro")
            return

        isbn = self.tree.item(item, "values")[0]

        win = tk.Toplevel(self.root)
        win.title("Comprar Livro")

        tk.Label(win, text="Quantidade").grid(row=0, column=0)
        qtd = tk.Entry(win)
        qtd.grid(row=0, column=1)

        def confirmar():
            try:
                quantidade = int(qtd.get())
                if quantidade <= 0:
                    raise ValueError

                venda = self.processar_compra(isbn, quantidade) if self.processar_compra else self.venda_dao.vender(isbn, quantidade)

                messagebox.showinfo(
                    "Compra realizada",
                    f"Livro: {venda['titulo']}\n"
                    f"Quantidade: {venda['quantidade']}\n"
                    f"Total: R$ {venda['valor_total']:.2f}"
                )

                win.destroy()
                if self.voltar is not None:
                    self.voltar()
                else:
                    self.carregar()

            except Exception as e:
                messagebox.showerror("Erro", str(e))

        tk.Button(win, text="Confirmar", command=confirmar).grid(row=1, column=0, columnspan=2)


    # =========================
    # EXCLUIR
    # =========================
    def excluir(self):
        item = self.tree.focus()

        if not item:
            return

        isbn = self.tree.item(item, "values")[0]

        if messagebox.askyesno("Confirmação", "Excluir?"):
            self.dao.excluir(isbn)
            self.carregar()

    # =========================
    # LIMPAR
    #=========================
    def limpar(self):
        for w in self.root.winfo_children():
            w.destroy()
