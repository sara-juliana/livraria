class Categoria:
    def __init__(self, codigo, descricao):
        self.codigo = codigo
        self.descricao = descricao

    def __str__(self):
        return self.descricao