from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

# Initialize Flask extensions without binding to the app yet
db = SQLAlchemy()
csrf = CSRFProtect()