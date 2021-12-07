from flask import Flask, render_template, request, redirect, session, flash, url_for

app = Flask(__name__)
app.secret_key = 'matheus'


class Jogo:
    def __init__(self, nome, categoria, console):
        self.__nome = nome
        self.__categoria = categoria
        self.__console = console

    @property
    def nome(self):
        return self.__nome

    @property
    def categoria(self):
        return self.__categoria

    @property
    def console(self):
        return self.__console


class Usuario:
    def __init__(self, user_id, nome, senha):
        self.__id = user_id
        self.__nome = nome
        self.__senha = senha

    @property
    def id(self):
        return self.__id

    @property
    def nome(self):
        return self.__nome

    @property
    def senha(self):
        return self.__senha


usuario1 = Usuario('mazzatheus', 'Matheus Matos', '12321')
usuario2 = Usuario('azzam221', 'Azzam Zao', 'azzamzam')
usuario3 = Usuario('math211', 'Mathias Camargo', 'mac1')

usuarios = {usuario1.id: usuario1,
            usuario2.id: usuario2,
            usuario3.id: usuario3}

jogo1 = Jogo('Super Mario', 'Ação', 'SNES')
jogo2 = Jogo('Pokemon Gold', 'RPG', 'GBA')
jogo3 = Jogo('GTA San Andreas', 'RPG', 'PS2')
lista = [jogo1, jogo2, jogo3]


@app.route("/")
def index():
    return render_template('lista.html', titulo='Jogos', jogos=lista)


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        # Usuário não está logado
        return redirect(url_for('login', proxima=url_for('novo')))
    else:
        # Usuário está logado
        return render_template('novo.html', titulo='Novo Jogo')


@app.route('/criar', methods=['POST', ])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST', ])
def autenticar():
    """ Valida se o id e senha do usuário estão cadastrados"""
    proxima_pagina = request.form['proxima']  # Se houver valor, atribui à variável
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            # Usuário Válido
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + ' logou com sucesso!')
            return redirect(proxima_pagina)
    # Usuário Inválido
    flash('ID ou Senha inválido!')
    if proxima_pagina:
        return redirect(url_for('login', proxima=proxima_pagina))
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))


app.run(debug=True)
