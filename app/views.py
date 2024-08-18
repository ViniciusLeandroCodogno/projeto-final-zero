from app import app, db
from flask import render_template, url_for, redirect, request
from app.forms import userForm, loginForm, postForm
from flask_login import login_user, logout_user, current_user
from app.models import Post, Comentario


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
        
        post = Post(
            mensagem=form.mensagem.data,
            user_id = current_user.id
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