from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv('.env')

app = Flask(__name__)

# Configurações
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATA_BASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Extensões
from .extensions import db, migrate, bcrypt, login_manager

db.init_app(app)
migrate.init_app(app, db)
bcrypt.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

from app.views import homepage
from app.models import Contato
