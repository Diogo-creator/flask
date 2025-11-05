from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

class Contato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_envio = db.Column(db.DateTime(), default=datetime.now)
    nome = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    assunto = db.Column(db.String(100), nullable=True)
    mensagem = db.Column(db.String(1000), nullable=True)
    respondido = db.Column(db.Integer, default=0)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    lastname = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    post = db.relationship('Post', backref=db.backref('user', lazy=True))
    comentario = db.relationship('Comentario', backref=db.backref('user', lazy=True))

    def get_id(self):
        return str(self.id)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mensagem = db.Column(db.String(1000), nullable=True)
    imagem = db.Column(db.String(50), nullable=True, default='default.png')
    data_postagem = db.Column(db.DateTime(), default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    comentario = db.relationship('Comentario', backref=db.backref('post', lazy=True))

    def mensagem_resumida(self):
        if len(self.mensagem) > 50:
            return self.mensagem[:50] + '...'
        else:
            return self.mensagem

class Comentario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comentario = db.Column(db.String(500), nullable=False)
    data_comentario = db.Column(db.DateTime(), default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))