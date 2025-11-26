from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, RadioField, SubmitField
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