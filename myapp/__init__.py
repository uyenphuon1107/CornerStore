import flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import stripe

# gives current directory of this file
basedir = os.path.abspath(os.path.dirname(__file__))
# instance of the Flask class
myapp_obj = flask.Flask(__name__)
myapp_obj.config.from_mapping(
    SECRET_KEY = 'it-dont-matter',
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS = False
)

myapp_obj.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51KwJCGIVxGuZvYFfhSYF6A2R8HPvG6ttxkhDCuTkQJxk31G7bIVzeBeM8QKuX2VI7N7rh7iwimycdWLZdGvMA5P4005cDABfsv'
myapp_obj.config['STRING_SECRET_KEY'] = 'sk_test_51KwJCGIVxGuZvYFf0YW5nfbMrKiW4fmwQZfpuOM1ai8b1y1CZb5OXKIFxbfGNhzW4DebQE2g7RC6ABu6Xq9NIC9D00eYLOFkSj'

stripe.api_key = myapp_obj.config['STRING_SECRET_KEY']

db = SQLAlchemy(myapp_obj)

login = LoginManager(myapp_obj)
login.login_view = 'login'

from myapp import routes, models, admin 
db.create_all()

