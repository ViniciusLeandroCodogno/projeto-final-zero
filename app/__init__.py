from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

import cloudinary
import cloudinary.uploader
import cloudinary.api


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '2b1d7a492ea2c51841aba3ea1c950fc35de92e8be6a3853f'

cloudinary.config(
  cloud_name = 'seu_cloud_name', 
  api_key = 'sua_api_key', 
  api_secret = 'seu_api_secret'
)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)


from app import views