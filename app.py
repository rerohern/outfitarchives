from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, PasswordField, TextAreaField, SelectMultipleField, SubmitField
from models import *
from extensions import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'archiveround2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///outfitarchive.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.route('/', methods=["GET", "POST"])
def index():
    return "ok, round 2 let's get building"