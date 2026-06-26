import tkinter as tk
from tkinter import ttk, messagebox

from dao.livro_digital_dao import LivroDigitalDAO
from dao.categoria_dao import CategoriaDAO
from dao.editora_dao import EditoraDAO
from dao.autor_dao import AutorDAO
from models.livro import LivroDigital

from dao.venda_dao import VendaDAO


class LivroDigitalView:

    def __init__(self, root, voltar, processar_compra=None):
        self.root = root
        self.dao = LivroDigitalDAO()
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

        tk.Label(self.root, text="💻 Livros Digitais", font=("Arial", 14, "bold")).pack(pady=10)

        frame = tk.Frame(self.root)
        frame.pack()

        # LISTAGEM ENXUTA
        self.tree = ttk.Treeview(
            frame,
            columns=("isbn", "titulo", "categoria", "editora", "formato", "tamanho", "qtd", "preco"),
            show="headings"
        )

        for c in self.tree["columns"]:
            self.tree.heading(c, text=c.upper())

        self.tree.pack()

        btn = tk.Frame(self.root)
        btn.pack(pady=10)

        tk.Button(btn, text="Atualizar", command=self.carregar).grid(row=0, column=0)
        tk.Button(btn, text="Novo", command=self.adicionar).grid(row=0, column=1)
        tk.Button(btn, text="Detalhes", command=self.detalhes).grid(row=0, column=2)
        tk.Button(btn, text="Editar", command=self.editar).grid(row=0, column=3)
        tk.Button(btn, text="Atualizar Livro", command=self.atualizar_livro).grid(row=0, column=4)
        tk.Button(btn, text="Comprar", command=self.comprar).grid(row=0, column=5)
        tk.Button(btn, text="Excluir", command=self.excluir).grid(row=0, column=6)
        tk.Button(btn, text="Voltar", command=self.voltar).grid(row=0, column=7)

        self.carregar()

    # =========================
    # LISTAGEM
    # =========================
    def carregar(self):
        self.carregar_dados()
        self.tree.delete(*self.tree.get_children())

        for l in self.dao.listar():
            self.tree.insert("", "end", values=(
                l[0],  # isbn
                l[1],  # titulo
                l[2],  # categoria
                l[3],  # editora
                l[4],  # formato
                l[5],  # tamanho
                l[6],  # quantidade
                f"R$ {float(l[7]):.2f}" if l[7] else "R$ 0.00"
            ))

    # =========================
    # DETALHES COMPLETOS
    # =========================
    def detalhes(self):
        item = self.tree.focus()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um livro")
            return

        isbn = self.tree.item(item, "values")[0]
        livro = self.dao.detalhes(isbn)

        if not livro:
            return

        win = tk.Toplevel(self.root)
        win.title("Detalhes Livro Digital")

        texto = f"""
ISBN: {livro[0]}
Título: {livro[1]}
Ano: {livro[2]}
Preço: R$ {livro[3]}
Quantidade: {livro[4]}

Categoria: {livro[5]}
Editora: {livro[6]}

Formato: {livro[7]}
Tamanho MB: {livro[8]}
"""

        tk.Label(win, text=texto, justify="left", font=("Arial", 10)).pack(padx=10, pady=10)

    # =========================
    # ADICIONAR
    # =========================
    def adicionar(self):
        self.carregar_dados()

        win = tk.Toplevel(self.root)
        win.title("Novo Livro Digital")

        tk.Label(win, text="ISBN").grid(row=0, column=0)
        isbn = tk.Entry(win)
        isbn.grid(row=0, column=1)

        tk.Label(win, text="Título").grid(row=1, column=0)
        titulo = tk.Entry(win)
        titulo.grid(row=1, column=1)

        tk.Label(win, text="Ano").grid(row=2, column=0)
        ano = tk.Entry(win)
        ano.grid(row=2, column=1)

        tk.Label(win, text="Categoria").grid(row=3, column=0)
        cat = ttk.Combobox(win, values=[c.descricao for c in self.categorias], state="readonly")
        cat.grid(row=3, column=1)

        tk.Label(win, text="Editora").grid(row=4, column=0)
        edi = ttk.Combobox(win, values=[e.razao_social for e in self.editoras], state="readonly")
        edi.grid(row=4, column=1)

        tk.Label(win, text="Autores").grid(row=5, column=0)
        lb = tk.Listbox(win, selectmode="multiple")
        lb.grid(row=5, column=1)

        for a in self.autores:
            lb.insert(tk.END, a.nome)

        tk.Label(win, text="Formato").grid(row=6, column=0)
        formato = tk.Entry(win)
        formato.grid(row=6, column=1)

        tk.Label(win, text="Tamanho MB").grid(row=7, column=0)
        tamanho = tk.Entry(win)
        tamanho.grid(row=7, column=1)

        tk.Label(win, text="Qtd").grid(row=8, column=0)
        qtd = tk.Entry(win)
        qtd.grid(row=8, column=1)

        tk.Label(win, text="Preco").grid(row=9, column=0)
        preco = tk.Entry(win)
        preco.grid(row=9, column=1)

        def salvar():

            if not isbn.get() or not titulo.get():
                messagebox.showerror("Erro", "Campos obrigatórios")
                return

            cat_obj = next((c for c in self.categorias if c.descricao == cat.get()), None)
            edi_obj = next((e for e in self.editoras if e.razao_social == edi.get()), None)

            autores_obj = [self.autores[i] for i in lb.curselection()]

            if not cat_obj or not edi_obj:
                messagebox.showerror("Erro", "Selecione categoria e editora")
                return

            try:
                livro = LivroDigital(
                    isbn.get(),
                    titulo.get(),
                    int(ano.get() or 2024),
                    edi_obj,
                    int(qtd.get() or 1),
                    float(preco.get() or 0),
                    cat_obj,
                    autores_obj,
                    formato.get(),
                    float(tamanho.get() or 0)
                )

                self.dao.salvar(livro)
                win.destroy()
                self.carregar()
            except ValueError as e:
                messagebox.showerror("Erro", str(e))
            except Exception as e:
                messagebox.showerror("Erro", f"NÃ£o foi possÃ­vel salvar o livro digital: {e}")

        tk.Button(win, text="Salvar", command=salvar).grid(row=10, column=0, columnspan=2)

    def atualizar_livro(self):
        item = self.tree.focus()

        if not item:
            messagebox.showwarning("Aviso", "Selecione um livro")
            return

        isbn = self.tree.item(item, "values")[0]

        win = tk.Toplevel(self.root)
        win.title("Atualizar Livro Digital")

        tk.Label(win, text="Quantidade").grid(row=0, column=0)
        qtd = tk.Entry(win)
        qtd.grid(row=0, column=1)

        tk.Label(win, text="Preco").grid(row=1, column=0)
        preco = tk.Entry(win)
        preco.grid(row=1, column=1)

        def salvar():
            try:
                qtd_val = int(qtd.get())
                preco_val = float(preco.get())

                if qtd_val < 0:
                    raise ValueError("Quantidade nao pode ser negativa")

                self.dao.atualizar_qtd_preco(isbn, qtd_val, preco_val)
                win.destroy()
                self.carregar()
            except ValueError as e:
                messagebox.showerror("Erro", str(e))

        tk.Button(win, text="Salvar", command=salvar).grid(row=2, column=0, columnspan=2)

    # =========================
    # EDITAR
    # =========================
    def editar(self):
        item = self.tree.focus()
        if not item:
            return

        isbn = self.tree.item(item, "values")[0]

        win = tk.Toplevel(self.root)
        win.title("Editar")

        tk.Label(win, text="Título").grid(row=0, column=0)
        titulo = tk.Entry(win)
        titulo.grid(row=0, column=1)

        tk.Label(win, text="Formato").grid(row=1, column=0)
        formato = tk.Entry(win)
        formato.grid(row=1, column=1)

        tk.Label(win, text="Tamanho MB").grid(row=2, column=0)
        tamanho = tk.Entry(win)
        tamanho.grid(row=2, column=1)

        def salvar():
            self.dao.atualizar(
                isbn,
                titulo.get(),
                formato.get(),
                float(tamanho.get() or 0)
            )
            win.destroy()
            self.carregar()

        tk.Button(win, text="Salvar", command=salvar).grid(row=3, column=0, columnspan=2)

    def comprar(self):
        item = self.tree.focus()

        if not item:
            messagebox.showwarning("Aviso", "Selecione um livro")
            return

        isbn = self.tree.item(item, "values")[0]

        win = tk.Toplevel(self.root)
        win.title("Comprar Livro Digital")

        tk.Label(win, text="Quantidade").grid(row=0, column=0)
        qtd = tk.Entry(win)
        qtd.grid(row=0, column=1)

        def confirmar():
            try:
                quantidade = int(qtd.get())

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

    def limpar(self):
        for w in self.root.winfo_children():
            w.destroy()
