import tkinter as tk
from tkinter import ttk

from dao.venda_dao import VendaDAO


class RelatorioVendasView:

    def __init__(self, root, voltar):
        self.root = root
        self.dao = VendaDAO()
        self.voltar = voltar
        self.tela()

    def tela(self):
        self.limpar()

        tk.Label(self.root, text="📊 Relatório de Livros Vendidos", font=("Arial", 14, "bold")).pack(pady=10)

        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(
            frame,
            columns=("codigo", "titulo", "tipo", "quantidade", "valor_unitario", "valor_total", "data_venda"),
            show="headings"
        )

        colunas = {
            "codigo": "Código",
            "titulo": "Título",
            "tipo": "Tipo",
            "quantidade": "Qtd",
            "valor_unitario": "Valor Unit.",
            "valor_total": "Valor Total",
            "data_venda": "Data"
        }

        for col, text in colunas.items():
            self.tree.heading(col, text=text)
            self.tree.column(col, width=110, anchor="center")

        self.tree.pack(fill="both", expand=True)

        self.carregar()

        footer = tk.Frame(self.root)
        footer.pack(pady=10)

        total_vendas = self.dao.total_vendas()
        total_caixa = self.dao.total_caixa()

        tk.Label(footer, text=f"Total de vendas: {total_vendas}", font=("Arial", 11, "bold")).pack(side="left", padx=10)
        tk.Label(footer, text=f"Caixa acumulado: R$ {total_caixa:.2f}", font=("Arial", 11, "bold")).pack(side="left", padx=10)
        tk.Button(footer, text="Voltar", command=self.voltar).pack(side="right", padx=10)

    def carregar(self):
        self.tree.delete(*self.tree.get_children())

        for venda in self.dao.listar_vendas():
            codigo, titulo, tipo, quantidade, valor_unitario, valor_total, data_venda = venda
            self.tree.insert("", "end", values=(
                codigo,
                titulo,
                tipo,
                quantidade,
                f"R$ {float(valor_unitario):.2f}",
                f"R$ {float(valor_total):.2f}",
                data_venda
            ))

    def limpar(self):
        for w in self.root.winfo_children():
            w.destroy()
