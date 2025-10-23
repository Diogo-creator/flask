from flask import flash
from flask_wtf import FlaskForm
from sqlalchemy.exc import IntegrityError
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import Contato, User
from app import db, bcrypt

# Formulário de Registro de Usuário
class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmation_password = StringField('Confirmation Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    btnSubmit = SubmitField('Register')

    # Validação personalizada para garantir que o email não esteja duplicado
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different email address.')
    
        # Método para salvar o usuário no banco de dados
    def save(self):
        password = bcrypt.generate_password_hash(self.password.data.encode('utf-8'))
        user = User(
            username=self.username.data,
            lastname=self.lastname.data,
            email=self.email.data,
            password=password
        )
        try:
            db.session.add(user)
            db.session.commit()
            return user
        except IntegrityError:
            db.session.rollback()
            flash("Erro: nome de usuário ou e-mail já cadastrado.")
            return None

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    btnSubmit = SubmitField('Login')

    def login(self):
        #recuperar o usuário do banco de dados
        user = User.query.filter_by(email=self.email.data).first()
        #verificar se usuário existe e senha está correta
        if user:
            if bcrypt.check_password_hash(user.password, self.password.data.encode('utf-8')):
                return user
            else:
                raise Exception("Senha incorreta")
        else:
            raise Exception("Usuário não encontrado")

        
class ContatoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    mensagem = StringField('Mensagem', validators=[DataRequired()])
    assunto = StringField('Assunto', validators=[DataRequired()])
    btnSubmit = SubmitField('Enviar')

    def save(self):
        contato = Contato(
            nome=self.nome.data,
            email=self.email.data,
            assunto=self.assunto.data,
            mensagem=self.mensagem.data
        )
        db.session.add(contato)
        db.session.commit()