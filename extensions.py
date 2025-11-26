from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_login import LoginManager

# Initialize Flask extensions without binding to the app yet
db = SQLAlchemy()
csrf = CSRFProtect()

login_manager = LoginManager()