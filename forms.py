from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length

class UserForm(FlaskForm):
    """UserForm will be the register and login form"""
    username = StringField("Username",
        validators = [
            InputRequired(message = "Username is required!"),
            Length(min = 1, max = 100, message = "Username must be between 1 and 100 characters.")
        ]
    )
    password = PasswordField("Password",
        validators = [
            InputRequired(message = "Password is required!"),
            Length(min = 6, max = 30, message = "Password must be between 6 and 30 characters.")
        ]
    )

    