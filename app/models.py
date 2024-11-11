from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=True)
    sobrenome = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    senha = db.Column(db.String, nullable=True)
    posts = db.relationship('Post', backref='user', lazy=True)
    petgrams = db.relationship('Petgram', backref='user', lazy=True)
    comentarios_petgram = db.relationship('ComentarioPetgram', backref='user', lazy=True)
    foto_perfil = db.Column(db.String(120), default='default.jpg')

    def __repr__(self):
        return f"User('{self.id}', '{self.nome}', '{self.sobrenome}', '{self.email}', '{self.foto_perfil}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mensagem = db.Column(db.String, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    imagem = db.Column(db.String, nullable=True)
    categoria = db.Column(db.String(50), nullable=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Post('{self.mensagem}', '{self.imagem}', '{self.categoria}')"

class Comentario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    
    user = db.relationship('User', backref='comentarios')
    post = db.relationship('Post', backref='comentarios')

class Petgram(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mensagem = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comentarios = db.relationship('ComentarioPetgram', backref='petgram', lazy=True)
    imagem = db.Column(db.String, nullable=True)
    categoria_petgram = db.Column(db.String(50), nullable=True)
    data_cricao = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Post('{self.mensagem}', '{self.imagem}', '{self.categoria_petgram}')" 

class ComentarioPetgram(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    petgram_id = db.Column(db.Integer, db.ForeignKey('petgram.id'), nullable=False)
