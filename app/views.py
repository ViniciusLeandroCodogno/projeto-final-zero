from app import app, db, bcrypt
from flask import render_template, send_from_directory, url_for, redirect, request, flash
from app.forms import userForm, loginForm, postForm, petgramForm
from flask_login import login_user, logout_user, current_user, login_required
from app.models import Post, Comentario, Petgram, ComentarioPetgram, User
from werkzeug.utils import secure_filename
from flask import current_app
import os

UPLOAD_FOLDER = os.path.join(app.root_path, 'static','uploads')
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def homepage():
    if current_user.is_authenticated:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.senha, form.senha.data):
            login_user(user, remember=True)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('postNovo'))
        else:
            flash('Falha no Login. Verifique seu e-mail e senha', 'danger')
            return redirect(url_for('login'))
    return render_template('login/login.html', form=form)

@app.route('/cadastro/', methods=['GET', 'POST'])
def cadastro():
    form = userForm()
    if form.validate_on_submit():
        user = form.save()
        login_user(user, remember=True)
        return redirect(url_for('homepage'))
    return render_template('login/cadastro.html', form=form)

@app.route('/sair/')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/post/novo/', methods=['GET', 'POST'])
def postNovo():
    form = postForm()
    if form.validate_on_submit():
        imagem = None
        if 'imagem' in request.files:
            file = request.files['imagem']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                
                imagem = filename
        
        post = Post(
            mensagem=form.mensagem.data,
            user_id=current_user.id,
            imagem=imagem,
            categoria=form.categoria.data
        )
        db.session.add(post)
        db.session.commit()
        
        return redirect(url_for('postLista'))
    
    return render_template('blog/blog_post.html', form=form)

@app.route('/post/lista/', methods=['GET', 'POST'])
def postLista():
    posts = Post.query.order_by(Post.data_criacao.desc()).limit(5).all()
    return render_template('blog/blog.html', posts=posts)

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

    return render_template('blog/blog_editar.html', post=post)

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

@app.route('/petgram/', methods=['GET', 'POST'])
def petgramNovo():
    form = petgramForm()
    if form.validate_on_submit():
        imagem = None
        if 'imagem' in request.files:
            file = request.files['imagem']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                imagem = filename
        
        petgram = Petgram(
            mensagem=form.mensagem.data,
            user_id=current_user.id,
            imagem=imagem,
            categoria_petgram=form.categoria_petgram.data

        )
        db.session.add(petgram)
        db.session.commit()
        
        return redirect(url_for('petgramLista'))
    
    return render_template('petgram/petgram_post.html', form=form)

@app.route('/petgram/lista/', methods=['GET', 'POST'])
def petgramLista():
    petgrams = Petgram.query.order_by(Petgram.data_cricao.desc()).limit(5).all()
    return render_template('petgram/petgram.html', petgrams=petgrams)

@app.route('/comentar_petgram/<int:petgram_id>', methods=['POST'])
def comentar_petgram(petgram_id):
    petgram = Petgram.query.get_or_404(petgram_id)
    conteudo = request.form.get('conteudo')
    
    comentario = ComentarioPetgram(conteudo=conteudo, user_id=current_user.id, petgram_id=petgram.id)
    db.session.add(comentario)
    db.session.commit()
    
    return redirect(url_for('petgramLista'))

@app.route('/editar_petgram/<int:petgram_id>', methods=['GET', 'POST'])
def editar_petgram(petgram_id):
    petgram = Petgram.query.get_or_404(petgram_id)
    if petgram.user_id != current_user.id:
        return redirect(url_for('petgram_lista')) 

    if request.method == 'POST':
        petgram.mensagem = request.form.get('mensagem')
        db.session.commit()
        return redirect(url_for('petgramLista'))

    return render_template('petgram/petgram_editar.html', petgram=petgram)

@app.route('/excluir_petgram/<int:petgram_id>', methods=['POST'])
def excluir_petgram(petgram_id):
    petgram = Petgram.query.get_or_404(petgram_id)
    if petgram.user_id == current_user.id:
        db.session.delete(petgram)
        db.session.commit()
    return redirect(url_for('petgramLista'))

@app.route('/editar_comentario_petgram/<int:comentario_id>', methods=['GET', 'POST'])
def editar_comentario_petgram(comentario_id):
    comentario = ComentarioPetgram.query.get_or_404(comentario_id)
    if comentario.user_id != current_user.id:
        return redirect(url_for('petgram_lista')) 

    if request.method == 'POST':
        comentario.conteudo = request.form.get('conteudo')
        db.session.commit()
        return redirect(url_for('petgramLista'))

    return render_template('editar_comentario_petgram.html', comentario=comentario)

@app.route('/excluir_comentario_petgram/<int:comentario_id>', methods=['POST'])
def excluir_comentario_petgram(comentario_id):
    comentario = ComentarioPetgram.query.get_or_404(comentario_id)
    if comentario.user_id == current_user.id:
        db.session.delete(comentario)
        db.session.commit()
    return redirect(url_for('petgramLista'))

@app.route('/repteis/')
def repteis():
    posts = Post.query.filter_by(categoria='Répteis').all()
    return render_template('blog/blog_repteis.html', posts=posts)

@app.route('/mamiferos/')
def mamiferos():
    posts = Post.query.filter_by(categoria='Mamíferos').all()
    return render_template('blog/blog_mamiferos.html', posts=posts)

@app.route('/aquaticos/')
def aquaticos():
    posts = Post.query.filter_by(categoria='Aquáticos').all()
    return render_template('blog/blog_aquaticos.html', posts=posts)

@app.route('/aves/')
def aves():
    posts = Post.query.filter_by(categoria='Aves').all()
    return render_template('blog/blog_aves.html', posts=posts)


# Nave Petgram

@app.route('/repteis/petgram/')
def repteis_petgram():
    petgrams = Petgram.query.filter_by(categoria_petgram='Répteis').all()
    return render_template('petgram/petgram_repteis.html', petgrams=petgrams)

@app.route('/mamiferos/petgram/')
def mamiferos_petgram():
    petgrams = Petgram.query.filter_by(categoria_petgram='Mamíferos').all()
    return render_template('petgram/petgram_mamiferos.html', petgrams=petgrams)

@app.route('/aquaticos/petgram/')
def aquaticos_petgram():
    petgrams = Petgram.query.filter_by(categoria_petgram='Aquáticos').all()
    return render_template('petgram/petgram_aquaticos.html', petgrams=petgrams)

@app.route('/aves/petgram/')
def aves_petgram():
    petgrams = Petgram.query.filter_by(categoria_petgram='Aves').all()
    return render_template('petgram/petgram_aves.html', petgrams=petgrams)

