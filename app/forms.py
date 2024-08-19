from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed
from app import db, bcrypt
from app.models import User, Post, Petgram
from cloudinary.uploader import upload
from flask import url_for


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
    imagem = FileField('Imagem', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    btnSubmit = SubmitField('Enviar')

    def save(self, user_id):
        imagem_url = url_for('static', filename='images/')
        if self.imagem.data:
            upload_result = upload(self.imagem.data)
            imagem_url = upload_result['url']
        post = Post(
            mensagem=self.mensagem.data,
            user_id=user_id,
            imagem_url=imagem_url
        )
        db.session.add(post)
        db.session.commit()


class petgramForm(FlaskForm):
    mensagem = StringField('Mensagem', validators=[DataRequired()])
    imagem = FileField('Imagem', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    btnSubmit = SubmitField('Enviar')

    def save(self, user_id):
        imagem_url = url_for('static', filename='images/')
        if self.imagem.data:
            upload_result = upload(self.imagem.data)
            imagem_url = upload_result['url']
        petgram = Petgram(
            mensagem=self.mensagem.data,
            user_id=user_id,
            imagem_url=imagem_url
        )
        db.session.add(petgram)
        db.session.commit()