from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory
from dao import JogoDao, UsuarioDao
from flask_mysqldb import MySQL
from models import Jogo
import os
import time

app = Flask(__name__)
app.secret_key = 'matheus'
app.config['MYSQL_HOST'] = "127.0.0.1"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "Mazzatheus1!"
app.config['MYSQL_DB'] = "jogoteca"
app.config['MYSQL_PORT'] = 3306
app.config['UPLOAD_PATH'] = os.path.dirname(os.path.abspath(__file__)) + '/uploads'

db = MySQL(app)
jogo_dao = JogoDao(db)
usuario_dao = UsuarioDao(db)


@app.route("/")
def index():
    lista = jogo_dao.listar()
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
    jogo = jogo_dao.salvar(jogo)
    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')
    return redirect(url_for('index'))


@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)


@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        # Usuário não está logado
        return redirect(url_for('login', proxima=url_for('editar')))
    else:
        # Usuário está logado
        jogo = jogo_dao.busca_por_id(id)
        nome_imagem = recupera_imagem(id)
        return render_template('editar.html', titulo='Editando Jogo', jogo=jogo, capa_jogo=nome_imagem or 'capa_padrao.jpg')


@app.route('/atualizar', methods=['POST', ])
def atualizar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    id = request.form['id']
    jogo = Jogo(nome, categoria, console, id)  # Diferente de criar, aqui passa o id pois é um jogo já existente

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    deleta_arquivo(id)
    arquivo.save(f'{upload_path}/capa{id}-{timestamp}.jpg')
    jogo_dao.salvar(jogo)
    return redirect(url_for('index'))


@app.route('/deletar/<int:id>')
def deletar(id):
    jogo_dao.deletar(id)
    flash("O jogo foi removido com sucesso!")
    return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST', ])
def autenticar():
    """ Valida se o id e senha do usuário estão cadastrados"""
    proxima_pagina = request.form['proxima']  # Se houver valor, atribui à variável
    usuario = usuario_dao.buscar_por_id(request.form['usuario'])
    if usuario:
        if request.form['senha'] == usuario.senha:
            # Usuário Válido
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + ' logou com sucesso!')
            return redirect(proxima_pagina)
    # Usuário Inválido
    flash('ID ou Senha inválido!')
    return redirect(url_for('login', proxima=proxima_pagina))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))

def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo

def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    if arquivo:
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))

app.run(debug=True)
