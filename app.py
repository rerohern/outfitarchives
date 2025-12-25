from flask import Flask, render_template, request, flash, redirect, url_for, session
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
        form = AddClosetPieceForm()

        #creating a piece on submit
        if form.validate_on_submit():
            name = form.name.data
            category = form.category.data
            brand = form.brand.data
            year_made = form.year_made.data

            #acquisition form info
            year_acquired = form.year_acquired.data
            credit_type = form.credit_type.data
            store_name = form.store_name.data
            store_location = form.store_location.data
            from_who = form.from_who.data

            acquisition = Acquisition(
                year_acquired=year_acquired,
                credit_type=credit_type,
                store_name=store_name,
                store_location=store_location,
                from_who=from_who
            )   

            db.session.add(acquisition)
            db.session.commit()

            #generate piece code
            new_piece = ClosetPiece(
                name=name, 
                category=category, 
                brand=brand, 
                year_made=year_made,
                acquisition_id=acquisition.id
            )

            db.session.add(new_piece)
            db.session.commit()

            #adding photos 
            img_src = form.img_src.data
            alt_text = form.alt_text.data

            media = Media(
                img_src = img_src,
                alt_text = alt_text,
                media_type = "piece",
                closet_piece_id = new_piece.id
            )

            db.session.add(media)
            db.session.commit()

            flash(f"new closet piece added: {new_piece.name}!")

        #if something doesn't work
        elif request.method == "POST":
            for field, errors in form.errors.items():
                for error in errors:
                    flash(
                        f"Error in {getattr(form, field).label.text}: {error}",
                        "danger"
                    )

        return render_template("landing-admin.html", current_user=current_user, form=form)

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

@app.route('/closet-pieces', methods=["GET"])
def closet_pieces():
    pieces = ClosetPiece.query.all()

    if current_user.is_authenticated:
        return render_template("closet-pieces-admin.html", closet=pieces)
    else:
        return render_template("closet-pieces-public.html", closet=pieces)

@app.route('/edit-closet-piece/<string:code>', methods=["GET", "POST"])
def edit_closet_piece(code):
    piece = ClosetPiece.query.filter_by(code=code).first_or_404()
    form = AddClosetPieceForm(obj=piece)  # pre-populate piece fields

    if not current_user.is_authenticated:
        return render_template("unauthorized-public.html")

    # Prefill acquisition and media fields on GET
    if request.method == "GET":
        # Acquisition
        if piece.acquisition:
            form.year_acquired.data = piece.acquisition.year_acquired
            form.credit_type.data = piece.acquisition.credit_type
            form.store_name.data = piece.acquisition.store_name
            form.store_location.data = piece.acquisition.store_location
            form.from_who.data = piece.acquisition.from_who

        # Media (piece images)
        media = piece.piece_images[0] if piece.piece_images else None
        if media:
            form.img_src.data = media.img_src
            form.alt_text.data = media.alt_text

    if form.validate_on_submit():
        # --- Update piece fields ---
        piece.name = form.name.data
        piece.category = form.category.data
        piece.brand = form.brand.data
        piece.year_made = form.year_made.data or None
        piece.deaccessioned = form.deaccessioned.data
        piece.deaccessioned_notes = form.deaccessioned_notes.data or None

        # --- Update or create acquisition ---
        if piece.acquisition:
            acquisition = piece.acquisition
        else:
            acquisition = Acquisition()
            piece.acquisition = acquisition
            db.session.add(acquisition)

        acquisition.year_acquired = form.year_acquired.data or None
        acquisition.credit_type = form.credit_type.data
        acquisition.store_name = form.store_name.data
        acquisition.store_location = form.store_location.data
        acquisition.from_who = form.from_who.data

        # --- Update or create media ---
        media = piece.piece_images[0] if piece.piece_images else None
        if not media:
            media = Media(media_type="piece", closet_piece=piece)
            db.session.add(media)

        media.img_src = form.img_src.data
        media.alt_text = form.alt_text.data

        db.session.commit()
        flash(f"{piece.name} updated successfully!", "success")
        return redirect(url_for('closet_pieces'))

    return render_template("edit-piece.html", form=form, piece=piece)
   
@app.route('/log-outfit', methods=["GET", "POST"])
def log_outfit():
    form = LogOutfitForm()

    return render_template("log-outfit.html", form=form)

if __name__ == "__main__":
    with app.app_context():
        # db.create_all()  # db already initialized, commented out but for future reference
        app.run(debug=True)

