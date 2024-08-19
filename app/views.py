from app import app, db
from flask import render_template, url_for, redirect, request
from app.forms import userForm, loginForm, postForm, petgramForm
from flask_login import login_user, logout_user, current_user
from app.models import Post, Comentario, Petgram
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def homepage():
    form = loginForm()
    if form.validate_on_submit():
        user = form.login()
        login_user(user, remember=True)
        return redirect(url_for('homepage'))
    return render_template('index.html', form=form)

@app.route('/cadastro/', methods=['GET', 'POST'])
def cadastro():
    form = userForm()
    if form.validate_on_submit():
        user = form.save()
        login_user(user, remember=True)
        return redirect(url_for('homepage'))
    return render_template('cadastro.html', form=form)

@app.route('/sair/')
def logout():
    logout_user()
    return redirect(url_for('homepage'))

@app.route('/post/novo/', methods=['GET', 'POST'])
def postNovo():
    form = postForm()
    if form.validate_on_submit():
        imagem = request.files.get('imagem')
        if imagem and allowed_file(imagem.filename):
            filename = secure_filename(imagem.filename)
            imagem_path = os.path.join(UPLOAD_FOLDER, filename)
            imagem.save(imagem_path)
            imagem_url = url_for('static', filename='images/' + filename)
        else:
            imagem_url = None
        
        post = Post(
            mensagem=form.mensagem.data,
            imagem_url=imagem_url,
            user_id=current_user.id
        )
       
        db.session.add(post)
        db.session.commit()
        
        return redirect(url_for('postLista'))
    
    return render_template('post_novo.html', form=form)

@app.route('/post/lista/', methods=['GET', 'POST'])
def postLista():
    posts = Post.query.all()
    return render_template('post_lista.html', posts=posts)

@app.route('/comentar/<int:post_id>', methods=['POST'])
def comentar_post(post_id):
    post = Post.query.get_or_404(post_id)
    conteudo = request.form.get('conteudo')
    
    comentario = Comentario(conteudo=conteudo, user_id=current_user.id, post_id=post.id)
    db.session.add(comentario)
    db.session.commit()
    
    return redirect(url_for('postLista'))


@app.route('/editar_post/<int:post_id>', methods=['GET', 'POST'])
def editar_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        return redirect(url_for('postLista')) 

    if request.method == 'POST':
        post.mensagem = request.form.get('mensagem')
        db.session.commit()
        return redirect(url_for('postLista'))

    return render_template('editar_post.html', post=post)

@app.route('/excluir_post/<int:post_id>', methods=['POST'])
def excluir_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id == current_user.id:
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for('postLista'))

@app.route('/editar_comentario/<int:comentario_id>', methods=['GET', 'POST'])
def editar_comentario(comentario_id):
    comentario = Comentario.query.get_or_404(comentario_id)
    if comentario.user_id != current_user.id:
        return redirect(url_for('postLista'))

    if request.method == 'POST':
        comentario.conteudo = request.form.get('conteudo')
        db.session.commit()
        return redirect(url_for('postLista'))

    return render_template('editar_comentario.html', comentario=comentario)

@app.route('/excluir_comentario/<int:comentario_id>', methods=['POST'])
def excluir_comentario(comentario_id):
    comentario = Comentario.query.get_or_404(comentario_id)
    if comentario.user_id == current_user.id:
        db.session.delete(comentario)
        db.session.commit()
    return redirect(url_for('postLista'))

@app.route('/petgram/novo/', methods=['GET', 'POST'])
def petgramNovo():
    form = petgramForm()
    if form.validate_on_submit():
        imagem = request.files.get('imagem')
        if imagem and allowed_file(imagem.filename):
            filename = secure_filename(imagem.filename)
            imagem_path = os.path.join(UPLOAD_FOLDER, filename)
            imagem.save(imagem_path)
            imagem_url = url_for('static', filename='images/' + filename)
        else:
            imagem_url = None
        
        petgram = Petgram(
            mensagem=form.mensagem.data,
            imagem_url=imagem_url,
            user_id=current_user.id
        )
       
        db.session.add(petgram)
        db.session.commit()
        
        return redirect(url_for('petgramLista'))
    
    return render_template('petgram_novo.html', form=form)

@app.route('/petgram/lista/', methods=['GET', 'POST'])
def petgramLista():
    petgrams = Petgram.query.all()
    return render_template('petgram_lista.html', petgrams=petgrams)

@app.route('/comentar_petgram/<int:petgram_id>', methods=['POST'])
def comentar_petgram(petgram_id):
    petgram = Petgram.query.get_or_404(petgram_id)
    conteudo = request.form.get('conteudo')
    
    comentario = Comentario(conteudo=conteudo, user_id=current_user.id, petgram_id=petgram.id)
    db.session.add(comentario)
    db.session.commit()
    
    return redirect(url_for('petgramLista'))

@app.route('/editar_petgram/<int:petgram_id>', methods=['GET', 'POST'])
def editar_petgram(petgram_id):
    petgram = Petgram.query.get_or_404(petgram_id)
    if petgram.user_id != current_user.id:
        return redirect(url_for('petgramLista')) 

    if request.method == 'POST':
        petgram.mensagem = request.form.get('mensagem')
        db.session.commit()
        return redirect(url_for('petgramLista'))

    return render_template('editar_petgram.html', petgram=petgram)

@app.route('/excluir_petgram/<int:petgram_id>', methods=['POST'])
def excluir_petgram(petgram_id):
    petgram = Petgram.query.get_or_404(petgram_id)
    if petgram.user_id == current_user.id:
        db.session.delete(petgram)
        db.session.commit()
    return redirect(url_for('petgramLista'))

@app.route('/editar_comentario_petgram/<int:comentario_id>', methods=['GET', 'POST'])
def editar_comentario_petgram(comentario_id):
    comentario = Comentario.query.get_or_404(comentario_id)
    if comentario.user_id != current_user.id:
        return redirect(url_for('petgramLista'))

    if request.method == 'POST':
        comentario.conteudo = request.form.get('conteudo')
        db.session.commit()
        return redirect(url_for('petgramLista'))

    return render_template('editar_comentario.html', comentario=comentario)

@app.route('/excluir_comentario_petgram/<int:comentario_id>', methods=['POST'])
def excluir_comentario_petgram(comentario_id):
    comentario = Comentario.query.get_or_404(comentario_id)
    if comentario.user_id == current_user.id:
        db.session.delete(comentario)
        db.session.commit()
    return redirect(url_for('petgramLista'))
