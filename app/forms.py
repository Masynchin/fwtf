from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *


class LoginForm(FlaskForm):
    astronaut_id = IntegerField("id астронавта", validators=[DataRequired()])
    astronaut_pwd = PasswordField("Пароль астронавта", validators=[DataRequired()])
    captain_id = IntegerField("id капитана", validators=[DataRequired()])
    captain_pwd = PasswordField("Пароль капитана", validators=[DataRequired()])
    submit = SubmitField("Доступ")


class ImageForm(FlaskForm):
    image = FileField("Приложите фотографию", validators=[DataRequired()])
    submit = SubmitField("Отправить")

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Repeat password",
        validators=[DataRequired(), EqualTo("password")])
    surname = StringField("Surname", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    age = IntegerField("Age", validators=[DataRequired()])
    position = StringField("Position", validators=[DataRequired()])
    speciality = StringField("Speciality", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    submit = SubmitField("Доступ")
