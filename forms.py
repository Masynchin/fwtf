from flask_wtf import FlaskForm
from wtforms import IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    astronaut_id = IntegerField("id астронавта", validators=[DataRequired()])
    astronaut_pwd = PasswordField("Пароль астронавта", validators=[DataRequired()])
    captain_id = IntegerField("id капитана", validators=[DataRequired()])
    captain_pwd = PasswordField("Пароль капитана", validators=[DataRequired()])
    submit = SubmitField("Доступ")
