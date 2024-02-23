#GRUPO: Allan Santos, João Carlos e Murilo Costa

from flask import Flask, render_template, request, session, redirect, url_for
# render_template para carregar arquivos html pelo flask
# request para poder pegar os dados de formulário
# session para poder guardar valores nas variáveis de sessão do navegador da pessoa
from classes import Anime, Tema
from random import choice
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder="templates")
UPLOAD_FOLDER = os.path.join(os.getcwd(), './static/images')

# chave para criptografar as variáveis de sessão
app.secret_key = "LGBSBGKYW#TBRjGJKgkejhrg"

### CRIAÇÃO DOS OBJETOS ###
# considere que todos os objetos "temas" e "series" foram criados corretamente
discussao = Tema("Discussão")
conteudo = Tema("Conteudo")

anime_demonSlayer = Anime("Demon Slayer", "demonSlayer.png", "A redenção e a humanização de personagens considerados vilões.", "Demon Slayer explora a possibilidade de redenção para personagens considerados irredimíveis. A humanização dos antagonistas por meio de suas histórias de vida e lutas pessoais destaca a complexidade moral do mundo apresentado, enfatizando a importância do perdão e da compaixão mesmo em situações aparentemente sem esperança.")
discussao.add_discussao(anime_demonSlayer)

anime_OnePunchMan = Anime("One Punch Man", "onePunchMan.png", "A crítica à obsessão pela força e poder em detrimento de outros valores.","One Punch Man satiriza a obsessão pela força e o heroísmo convencional, questionando os valores atribuídos à força física e destacando a importância de outras habilidades, como inteligência e empatia, na construção de uma sociedade verdadeiramente equilibrada.")
discussao.add_discussao(anime_OnePunchMan)

anime_Naruto = Anime("Naruto", "Naruto.png", "A jornada do autoconhecimento e aceitação pessoal na formação de um verdadeiro líder."," Naruto narra a jornada de um jovem que passa de um pária a um líder respeitado, aprendendo a aceitar a si mesmo e a compreender as nuances de suas próprias emoções. O desenvolvimento de Naruto mostra como a autoaceitação e o entendimento de suas próprias fraquezas podem transformar-se em força e empatia para liderar os outros.")
discussao.add_discussao(anime_Naruto)

anime_DBZ = Anime("Dragon Ball Z", "DBZ.png", "A série conta a história de Son Goku, guerreiro que descobre ser parte de um legado de poderosos conquistadores alienígenas - e passa a defender seu planeta adotivo, a Terra, de outros seres igualmente superfortes e capazes de feitos descomunais.","any")
discussao.add_discussao(anime_DBZ)

anime_OnePiece = Anime("One Piece", "OnePiece.png", "A importância da liberdade e da aventura na busca de um sonho compartilhado.", "One Piece retrata a busca de indivíduos por liberdade e aventura em um mundo repleto de perigos e desafios. A ambição dos personagens principais de alcançar seus sonhos e explorar o desconhecido reflete a importância de seguir o próprio caminho e buscar a realização pessoal, inspirando os espectadores a perseguir seus próprios objetivos com paixão e determinação.")
conteudo.add_conteudo(anime_OnePiece)

anime_Tsubasa = Anime("Captain Tsubasa", "tsubasa.png", "A importância da determinação e da persistência no esporte e na vida.", "Captain Tsubasa ilustra a importância de nunca desistir, mesmo diante de obstáculos aparentemente insuperáveis. A tenacidade dos personagens em busca da excelência no futebol inspira os espectadores a perseverar em seus próprios esforços, demonstrando que a dedicação e a prática são fundamentais para alcançar o sucesso.")
conteudo.add_conteudo(anime_Tsubasa)

anime_JujutsuKaisen = Anime("Jujutsu Kaizen", "jujutsuKaizen.png", "A dualidade entre o bem e o mal na construção dos personagens.", "Jujutsu Kaisen apresenta personagens complexos que desafiam as noções tradicionais de bem e mal. A ambiguidade moral dos antagonistas destaca a importância da empatia e compreensão mútua, sugerindo que a distinção entre heróis e vilões muitas vezes se baseia nas circunstâncias e nas escolhas individuais.")
conteudo.add_conteudo(anime_JujutsuKaisen)

anime_BokuNoHero = Anime("Boku no Hero Academia", "BokuNoHero.png", "O valor da perseverança e autoaperfeiçoamento na jornada de um herói.", "Boku no Hero Academia ressalta a importância do esforço contínuo e do aprimoramento pessoal na busca de um objetivo maior. Os desafios enfrentados pelos personagens principais ilustram a ideia de que o verdadeiro heroísmo surge da vontade de superar limitações pessoais e se tornar um exemplo para os outros.")
conteudo.add_conteudo(anime_BokuNoHero)

catalogo = [conteudo, discussao]

### FIM DA CRIAÇÃO DOS OBJETOS ###

@app.route('/')
def home():
    # SE A CHAVE "login" NÃO EXISTIR DENTRO DO DICIONÁRIO session...
    if "login" not in session:
        # cria a chave "login" na session e coloca o valor False
        session["login"] = False
    
    # seleção aleatória da série destaque


    # chamar a template index.html passando pra ela a série destaque e o catálogo 
    conteudo = render_template('index.html', parCatalogo=catalogo)
    return conteudo

# como essa rota pode chegar vinda de um formulário, precisamos ativar os métodos 
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    # pode chegar nessa rota vindo de um formulário ou vindo de um link.
    # quando chegar nessa rota vindo de um formulário:
    if request.method == "POST":
        # vamos pegar o que foi preenchido no formulário
        # os campos do formulário ficam armazenados no dicionário request.form
        # as chaves do dicionário são os "name" dos campos do form na template
        # os valores do dicionário são as respostas que a pessoa preencheu nos campos
        if request.form["email"] == "eu@eu.com" and request.form["senha"] == "aaa":
            # Se a pessoa acertar o login, vai alterar a session "login" para True
            # Assim saberemos em qualquer página do site se a pessoa fez login ou não
            session["login"]=True
            # depois do login, chamamos o painel de gerenciamento passando pra ele o catálogo
            conteudo = render_template("dashboard.html",parCatalogo=catalogo)
        else:
            # Se errar o login:
            mensagem = "Login inválido"
            # chamamos o template de mensagem pra mostrar uma mensagem de erro
            conteudo = render_template("mensagem.html", parMensagem=mensagem)
    
    # esse elif pertence ao primeiro IF dessa def
    # quando chegar nessa rota via GET (por um link por exemplo) 
    # mas já ter feito login:
    elif request.method == "GET" and session["login"] == True:        
        # se já fez login pode acessar o painel de gerenciamento
        conteudo = render_template("dashboard.html",parCatalogo=catalogo)
    else:
        # quando chegar nessa rota sem ter feito login:
        mensagem = "Acesso negado"
        # não pode acessar o painel, 
        # por isso chamamos a template que mostra a mensagem de erro
        conteudo = render_template("mensagem.html", parMensagem=mensagem)

    # depois dos testes de login vai retornar o conteúdo correto:
    return conteudo

@app.route("/logout")
def logout():
    # primeiro verificamos se existe algum login na session
    # caso seja o primeiro acesso ao site e a pessoa digite o endereço do logout,
    # não vai ter a chave "login" dentro da session para alterar.

    # se a chave "login" existir dentro da session...
    if "login" in session:
        # altera o valor de "login" na session e coloca o valor False
        # isso vai efetivar o logout
        session["login"] = False    

    # repete os passos de carregamento da home depois de ter feito logout 
    conteudo = render_template('index.html', parCatalogo=catalogo)
    return conteudo

# Esta rota é responsável por carregar a página de modificação de um tema específico.
@app.route("/modificar_tema/<nome_do_tema>")
def modificar_tema(nome_do_tema):
    # Renderiza o template para modificar o tema, passando o nome do tema atual para preencher o formulário.
    conteudo = render_template("modificar_tema.html", nome_atual=nome_do_tema)
    return conteudo

# Rota para processar as modificações feitas no tema.
@app.route("/processar_tema", methods=["GET", "POST"])
def processar_tema():
    # Apenas realiza a operação se o método for POST (dados enviados do formulário).
    if request.method=="POST":
        # Itera por todos os temas no catálogo.
        for tema in catalogo:
            # Procura pelo tema que foi enviado pelo formulário.
            if tema.nome == request.form['nome_atual']:
                # Atualiza o nome do tema com o novo valor enviado.
                tema.nome = request.form["novo_nome_tema"]

        # Após a atualização, redireciona o usuário de volta para o dashboard.
        conteudo = render_template("dashboard.html",parCatalogo=catalogo)
    else:
        # Se a requisição não for POST, informa ao usuário que o acesso foi negado.
        mensagem =  "Acesso negado."
        conteudo = render_template("mensagem.html", parMensagem=mensagem)
    return conteudo

# Rota para excluir um tema específico.
@app.route("/excluir_tema", methods=["GET", "POST"])
def excluir_tema():
    # Apenas realiza a operação se o método for POST (dados enviados do formulário).
    if request.method=="POST":
        # Itera por todos os temas no catálogo.
        for tema in catalogo:
            # Procura pelo tema que foi enviado pelo formulário.
            if tema.nome == request.form['nome_atual']:
                # Remove o tema do catálogo.
                catalogo.remove(tema)                    
        # Após a exclusão, redireciona o usuário de volta para o dashboard.
        conteudo = render_template("dashboard.html",parCatalogo=catalogo)
    else:
        # Se a requisição não for POST, informa ao usuário que o acesso foi negado.
        mensagem =  "Acesso negado."
        conteudo = render_template("mensagem.html", parMensagem=mensagem)
    return conteudo

# Rota para adicionar um novo tema.
@app.route("/adicionar_tema", methods=["GET", "POST"])
def adicionar_tema():
    # Apenas realiza a operação se o método for POST (dados enviados do formulário).
    if request.method == "POST":
        nome_novo_tema = request.form["nome_novo_tema"]
        # Cria um novo objeto tema com o nome fornecido.
        novo_objeto_tema = Tema(nome=nome_novo_tema)
        # Adiciona o novo tema ao catálogo.
        catalogo.append(novo_objeto_tema)
        # Redireciona o usuário de volta para o dashboard.
        return redirect(url_for('dashboard'))
    else:
        # Se a requisição não for POST, informa ao usuário que o acesso foi negado.
        mensagem = "Acesso negado."
        conteudo = render_template("mensagem.html", parMensagem=mensagem)
        return conteudo


@app.route("/discussao_anime/<titulo_da_serie>")
def discussao_anime(titulo_da_serie):

    for tema in catalogo:
        for card in tema.conteudos or tema.discussoes:
            if card.titulo == titulo_da_serie:
                serie_atual = card
                
                break

    # Renderiza o template para modificar a série, passando a série selecionada para preencher o formulário.
    conteudo = render_template("discussao_anime.html", card_selecionada=serie_atual)
    return conteudo

@app.route("/adicionar_comentario", methods=["GET","POST"])
def adicionar_comentario():
    serie_atual = ""
    if request.method=="POST" or request.method=="GET":
        titulo_card = request.form['titulo_card']
        for tema in catalogo:
            for card in tema.conteudos or tema.discussoes:
                if card.titulo==titulo_card:
                    texto_do_comentario = request.form['comentario']
                    card.comentarios.append(texto_do_comentario)
                    serie_atual = card

    conteudo = render_template("discussao_anime.html", card_selecionada=serie_atual)
    return conteudo

@app.route("/modificar_serie/<titulo_da_card>")
def modificar_serie(titulo_da_card):
    # Procura pela série especificada no catálogo.
    for tema in catalogo:
        for card in tema.discussoes or tema.conteudos:
            if card.titulo == titulo_da_card:
                card_atual = card
                break
    # Renderiza o template para modificar a série, passando a série selecionada para preencher o formulário.
    conteudo = render_template("modificar_serie.html", serie_selecionada=card_atual)
    return conteudo

# Rota para processar as modificações feitas na série.
@app.route("/processar_serie", methods=["GET", "POST"])
def processar_serie():
    # Apenas realiza a operação se o método for POST (dados enviados do formulário).
    if request.method == "POST":
        # Itera por todos os temas e séries no catálogo.
        for tema in catalogo:
            for card in tema.conteudos or tema.discussoes:
                # Procura pela série que foi enviada pelo formulário.
                if card.titulo == request.form['titulo_atual']:
                    # Atualiza os detalhes da série com os novos valores enviados.
                    card.titulo = request.form["novo_titulo_serie"]
                    card.imagem = request.form["novo_imagem_serie"]
                    card.topico = request.form["novo_topico_serie"]
                    card.descricao = request.form["novo_argumento_serie"]
                    break
        # Após a atualização, redireciona o usuário de volta para o dashboard.
        conteudo = render_template("dashboard.html",parCatalogo=catalogo)
    else:
        # Se a requisição não for POST, informa ao usuário que o acesso foi negado.
        mensagem =  "Acesso negado."
        conteudo = render_template("mensagem.html", parMensagem=mensagem)
    return conteudo

# Rota para excluir uma série específica.
@app.route("/excluir_serie", methods=["GET", "POST"])
def excluir_serie():
    # Apenas realiza a operação se o método for POST (dados enviados do formulário).
    if request.method == "POST":
        # Itera por todos os temas e séries no catálogo.
        for tema in catalogo:
            for card in tema.conteudos or tema.discussoes:
                # Procura pela série que foi enviada pelo formulário.
                if card.titulo == request.form['titulo_atual']:
                    if tema.nome == 'Discussão':
                        tema.discussoes.remove(card)
                        break
                    else:
                        tema.conteudos.remove(card)   
                        break                 
        # Após a exclusão, redireciona o usuário de volta para o dashboard.
        conteudo = render_template("dashboard.html",parCatalogo=catalogo)
    else:
        # Se a requisição não for POST, informa ao usuário que o acesso foi negado.
        mensagem =  "Acesso negado."
        conteudo = render_template("mensagem.html", parMensagem=mensagem)
    return conteudo

# Rota para adicionar uma nova série.
@app.route("/adicionar_serie", methods=["GET", "POST"])
def adicionar_serie():

    def upload():
        file = request.files['imagem_upload']
        savePath = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
        file.save(savePath)

    # Apenas realiza a operação se o método for POST (dados enviados do formulário).
    if request.method == "POST":
        # Coleta todos os detalhes da nova série do formulário.
        titulo_nova_card = request.form["titulo_nova_card"]
        imagem_nova_card = request.form["imagem_nova_card"]
        upload()
        topico_nova_card = request.form["topico_nova_card"]
        descricao_nova_card = request.form["argumento_nova_card"]
        tema_associado = request.form["tema_associado"]
        
        # Cria um novo objeto série com os detalhes fornecidos.

        nova_objeto_card = Anime(titulo_nova_card, imagem_nova_card, topico_nova_card, descricao_nova_card)
        
        #Adiciona a nova série ao tema correto no catálogo.
        for tema in catalogo:
            if tema.nome == tema_associado:
                if tema.nome == 'Discussão':
                    tema.add_discussao(nova_objeto_card)
                    break
                else:
                    tema.add_conteudo(nova_objeto_card)
        
        # Após a adição, redireciona o usuário de volta para o dashboard.
        conteudo = render_template("dashboard.html",parCatalogo=catalogo)
    else:
        # Se a requisição não for POST, informa ao usuário que o acesso foi negado.
        mensagem = "Acesso negado."
        conteudo = render_template("mensagem.html", parMensagem=mensagem)
    return conteudo

# comentarios_geral = []
# @app.route("/adicionar_comentario", methods=["POST", "GET"])    
# def adicionar_comentario():
#     novo_comentario = request.form["comentario"]
#     comentarios_geral.append(novo_comentario)
#     conteudo = render_template("modificar_tema.html", comentarios_geral=parComentariosGeral)
#     return conteudo


# EXECUTAR O PROGRAMA (RODAR O SITE)
if __name__ == '__main__':
    app.run(debug=True)