from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, TextAreaField, RadioField, DateField, SubmitField, HiddenField
from wtforms.validators import DataRequired, EqualTo, Optional
from datetime import date

# set up form _________________________________________________________________________________

class SetPasswordForm(FlaskForm):
    password = PasswordField("set password", validators=[DataRequired()])
    confirm = PasswordField("confirm password", validators=[DataRequired()])
    submit = SubmitField("create account!")

# login form _________________________________________________________________________________

class LogInForm(FlaskForm):
    username = StringField("username", default="rero", render_kw={"type": "hidden"})
    password = PasswordField("password", validators=[DataRequired()], render_kw={"placeholder": "type password here"})
    remember_me = BooleanField("remember me")
    submit = SubmitField("access archive")


# add ClosetPiece form _________________________________________________________________________________

class AddClosetPieceForm(FlaskForm):
    #core info to create piece code
    name = StringField("item name", validators=[DataRequired()])
    category = RadioField("category", choices=[("tops", "tops"), ("bottoms", "bottoms"), ("shoes", "shoes"), ("dresses", "dresses"), ("accessories", "accessories")], validators=[DataRequired()])
    brand = StringField("brand", validators=[Optional()])
    year_made = StringField("year made", validators=[Optional()])

    #acquisition info
    credit_type = RadioField("acquisition type", choices=[("purchase", "purchase"), ("thrift", "thrift"), ("loan", "loan"), ("gift", "gift")], validators=[DataRequired()])
    store_name = StringField("store", validators=[Optional()])
    store_location = StringField("store location", validators=[Optional()])
    from_who = StringField("from who", validators=[Optional()])
    year_acquired = IntegerField("year acquired", validators=[Optional()])

    #deaccession info
    deaccessioned = BooleanField("deaccessioned", validators=[Optional()])
    deaccessioned_notes = StringField("notes", validators=[Optional()])

    #media info
    img_src = StringField("img src pathway", render_kw={"placeholder": "e.g. media/folder/image-name.jpg"}, validators=[Optional()])
    alt_text = StringField("alt text (200 char max)", validators=[Optional()])
    texture_img_src = StringField("texture img src pathway", render_kw={"placeholder": "textured image"}, validators=[Optional()])
    texture_alt_text = StringField("alt text (200 char max)", validators=[Optional()])


    submit = SubmitField("add piece", render_kw={"class": "form-submit-button"})

# add Outfit form _________________________________________________________________________________

class LogOutfitForm(FlaskForm):
    # --- Core info (used to generate outfit code) ---
    date_worn = DateField(
        "date worn",
        default=date.today,
        validators=[DataRequired()]
    )

    special_toggle = BooleanField(
        "special",
        validators=[Optional()]
    )

    # --- Outfit details ---
    notes = TextAreaField(
        "notes",
        validators=[Optional()]
    )

    tags = StringField(
        "tags",
        validators=[Optional()]
    )

    # --- Hidden fields (JS-controlled) ---
    outfit_code = HiddenField()   # optional (if you want frontend access)
    media_data = HiddenField()    # JSON string from drag-and-drop

    # --- Submit ---
    submit = SubmitField(
        "add outfit",
        render_kw={"class": "form-submit-button"}
    )

# add Outfit Media forms ________________________________________________________________________________

class BaseMediaForm(FlaskForm):
    #image base
    img_src = StringField("img src pathway", render_kw={"placeholder": "e.g. media/folder/image-name.jpg"}, validators=[Optional()])
    alt_text = StringField("alt text (200 char max)", validators=[Optional()])
    media_type = HiddenField()
    view = HiddenField()

class OutfitMediaForm(BaseMediaForm):
    media_type = "outfit"
    view = RadioField("view", choices=[("front", "front"), ("left", "left"), ("back", "back"), ("right", "right")], validators=[DataRequired()])

class AltOutfitMediaForm(BaseMediaForm):
    media_type = "outfit_alt"
    view = RadioField("view", choices=[("front", "front"), ("left", "left"), ("back", "back"), ("right", "right")], validators=[DataRequired()])

class OutfitTextureMediaForm(BaseMediaForm):
    media_type = "texture"

class OutfitTextureMediaForm(BaseMediaForm):
    media_type = "month"



