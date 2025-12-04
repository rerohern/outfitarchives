from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, TextAreaField, RadioField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Optional

# set up form _________________________________________________________________________________

class SetPasswordForm(FlaskForm):
    password = PasswordField("set password", validators=[DataRequired()])
    confirm = PasswordField("confirm password", validators=[DataRequired()])
    submit = SubmitField("create account!")

# login form _________________________________________________________________________________

class LogInForm(FlaskForm):
    username = StringField("username", default="rero", render_kw={"type": "hidden"})
    password = PasswordField("password", validators=[DataRequired()])
    remember_me = BooleanField("remember me")
    submit = SubmitField("access archive")


# add ClosetPiece form _________________________________________________________________________________

class AddClosetPieceForm(FlaskForm):
    #core info to create piece code
    name = StringField("item name", validators=[DataRequired()])
    category = RadioField("category", choices=[("tops", "tops"), ("bottoms", "bottoms"), ("shoes", "shoes"), ("dresses", "dresses"), ("accessories", "accessories")], validators=[DataRequired()])
    brand = StringField("brand", validators=[Optional()])
    year_made = IntegerField("year made", validators=[Optional()])

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


    submit = SubmitField("add piece")

