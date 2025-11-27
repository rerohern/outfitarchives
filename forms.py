from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, TextAreaField, RadioField, SubmitField
from wtforms.validators import DataRequired, EqualTo

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
    brand = StringField("brand")
    year_made = IntegerField("year made")

    #acquisition info
    credit_type = RadioField("acquisition type", choices=[("purchase", "purchase"), ("thrift", "thrift"), ("loan", "loan"), ("gift", "gift")], validators=[DataRequired()])
    store_name = StringField("store")
    store_location = StringField("store location")
    from_who = StringField("from who")
    year_acquired = IntegerField("year acquired")

    #media info
    img_src = StringField("img src pathway")

    submit = SubmitField("add piece")

