from flask import Flask, render_template, request
from extensions import db, csrf

app = Flask(__name__)
app.config['SECRET_KEY'] = 'archiveround2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///outfitarchive.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize extensions
db.init_app(app)
csrf.init_app(app)

# importing models after db is initialized
from models import ClosetPiece

# routes __________________________________________________________________________________

@app.route('/', methods=["GET", "POST"])
@app.route('/home', methods=["GET", "POST"])
def index():
    return render_template("landing-public.html")

@app.route('/setup', methods=["GET"])
def setup():
    return render_template("setup.html")