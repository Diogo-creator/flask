from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    last_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

    def get_id(self):
        return self.id
    
class Contato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_envio = db.Column(db.DateTime(), default=datetime.now)
    nome = db.Column(db.String(), nullable=True)
    email = db.Column(db.String(), nullable=True)
    assunto = db.Column(db.String(), nullable=True)
    mensagem = db.Column(db.String(), nullable=True)
    respondido = db.Column(db.Integer, default=0)