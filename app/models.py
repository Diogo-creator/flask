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

    def get_id(self):
        return str(self.id)
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))