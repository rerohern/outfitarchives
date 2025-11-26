from flask import Flask, render_template, request, flash, redirect, url_for
from extensions import db, csrf, login_manager
from forms import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user, login_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'archiveround2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///outfitarchive.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize extensions
db.init_app(app)
csrf.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

# importing models after db is initialized
from models import User, Media, ClosetPiece, Acquisition, OutfitPieces, Outfit

# loading users 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# routes __________________________________________________________________________________

@app.route('/', methods=["GET", "POST"])
@app.route('/home', methods=["GET", "POST"])
def index():
    if current_user.is_authenticated: 
        return render_template("landing-admin.html", current_user=current_user)

    else:
        return render_template("landing-public.html")

@app.route('/setup', methods=["GET", "POST"])
def setup():
    if User.query.filter_by(username='rero').first():
        flash("admin account already exists! log in for archival access")
        return redirect(url_for('login'))

    form = SetPasswordForm()
    if form.validate_on_submit():
        user = User(username='rero')
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('admin account created!')
        return redirect(url_for('login'))
    
    elif request.method == "POST":
        # if form submitted but validation fails
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", "danger")

    return render_template('setup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LogInForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username='rero').first()
        password = form.password.data

        #validate password data
        if not check_password_hash(user.password_hash, password):
            flash("oops, incorrect password!")
            return render_template("login.html", form=form)

        #log user in
        login_user(user, remember=form.remember_me.data)
        flash("accessed! redirecting to home page")
        return redirect(url_for("index"))

    return render_template("login.html", form=form)

@app.route('/logout', methods=["GET", "POST"])
def logout():
    if current_user.is_authenticated:
        logout_user() 
        flash("bye! xoxo", "info")
    return redirect(url_for("index"))

if __name__ == "__main__":
    with app.app_context():
        # db.create_all()  # db already initialized, commented out but for future reference
        app.run(debug=True)