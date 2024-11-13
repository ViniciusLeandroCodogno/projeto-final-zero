from flask import current_app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from werkzeug.utils import secure_filename
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app import db, bcrypt
from app.models import User, Post, Petgram
import os

class userForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    sobrenome = StringField('Sobrenome', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    confirmacao_senha = PasswordField('Confirmação da senha', validators=[DataRequired(), EqualTo('senha')])
    btnSubmit = SubmitField('Cadastrar')

    def validade_email(self, email):
        if User.query.filter(email=email.data).first():
            return ValidationError('Usuário já cadastrado com esse E-mail!!!')

    def save(self):
        senha = bcrypt.generate_password_hash(self.senha.data.encode('utf-8'))
        user = User(
            nome=self.nome.data,
            sobrenome=self.sobrenome.data,
            email=self.email.data,
            senha=senha
        )
        db.session.add(user)
        db.session.commit()
        return user

class loginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    btnSubmit = SubmitField('Login')

    def login(self):
        user = User.query.filter_by(email=self.email.data).first()
        if user and bcrypt.check_password_hash(user.senha, self.senha.data.encode('utf-8')):
            return user
        raise Exception('Usuário não encontrado ou senha incorreta!!!')

class postForm(FlaskForm):
    mensagem = StringField('Mensagem', validators=[DataRequired()])
    imagem = FileField('Imagem', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Imagens apenas!')])
    categoria = SelectField('Categoria', choices=[
        ('Répteis', 'Répteis'),
        ('Mamíferos', 'Mamíferos'),
        ('Aves', 'Aves'),
        ('Aquáticos', 'Aquáticos')
    ], validators=[DataRequired()])
    btnSubmit = SubmitField('Enviar')

    def save(self, user_id):
        imagem = None
        if self.imagem.data:
            file = self.imagem.data
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            imagem = filename
        
        post = Post(
            mensagem=self.mensagem.data,
            user_id=user_id,
            imagem=imagem,
            categoria=self.categoria.data 
        )
        db.session.add(post)
        db.session.commit()

class petgramForm(FlaskForm):
    mensagem = StringField('Mensagem', validators=[DataRequired()])
    imagem = FileField('Imagem', validators=[FileAllowed(['jpg', 'png'], 'Imagens apenas!')])
    categoria_petgram = SelectField('Categoria', choices=[
        ('Répteis', 'Répteis'),
        ('Mamíferos', 'Mamíferos'),
        ('Aves', 'Aves'),
        ('Aquáticos', 'Aquáticos')
    ], validators=[DataRequired()])
    btnSubmit = SubmitField('Enviar')

    def save(self, user_id):
        imagem = None
        if self.imagem.data:
            file = self.imagem.data
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            imagem = filename

        petgram = Petgram(
            mensagem=self.mensagem.data,
            user_id=user_id,
            imagem=imagem,
            categoria_petgram=self.categoria_petgram.data
        )
        db.session.add(petgram)
        db.session.commit()
