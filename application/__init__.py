from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from application.models import engine,Session

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expensesDB.db'
app.config['SECRET_KEY'] = 'jnnononibinoun5165ibijbIJBIBIJBIB'

# db = SQLAlchemy(app)


from application import routes


from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

from .models import User, SESSION

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return SESSION.query(User).get(int(user_id))