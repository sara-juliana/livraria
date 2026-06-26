from models.nacionalidade import Nacionalidade

class Autor:
    def __init__(self, passaporte, nome, nacionalidade: Nacionalidade):
        self.passaporte = passaporte
        self.nome = nome
        self.nacionalidade = nacionalidade
        
        
    def __str__(self):
        return self.nome
