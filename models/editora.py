class Editora:
    def __init__(self, cnpj, razao_social):
        self.cnpj = cnpj
        self.razao_social = razao_social
        
    def __str__(self):
        return self.razao_social