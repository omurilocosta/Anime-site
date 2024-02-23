class Anime:
    def __init__(self, titulo, imagem, topico, descricao):
        self.titulo = titulo
        self.imagem = imagem
        self.topico = topico
        self.descricao = descricao
        self.comentarios = []

class Tema:
    def __init__(self, nome):
        self.nome = nome
        self.discussoes = []
        self.conteudos = []

    def add_discussao(self, discussao):
        self.discussoes.append(discussao)

    def add_conteudo(self, conteudo):
        self.discussoes.append(conteudo)

    