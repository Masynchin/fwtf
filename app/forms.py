from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *


class LoginForm(FlaskForm):
    email = StringField("Почта", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    remember_me = BooleanField("Запомнить меня")
    submit = SubmitField("Войти")


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
    city_from = StringField("City From", validators=[DataRequired()])
    submit = SubmitField("Доступ")


class JobForm(FlaskForm):
    job           = StringField("Job Title", validators=[DataRequired()])
    team_leader   = IntegerField("Team Leader ID", validators=[DataRequired()])
    work_size     = IntegerField("Work Size", validators=[DataRequired()])
    collaborators = StringField("Collaborators", validators=[DataRequired()])
    category_id   = IntegerField("Category ID", validators=[DataRequired()])
    is_finished   = BooleanField("Is job finished?")
    submit        = SubmitField("Submit")


class DepartmentForm(FlaskForm):
    title   = StringField("Title", validators=[DataRequired()])
    chief   = IntegerField("Chief ID", validators=[DataRequired()])
    members = StringField("Members", validators=[DataRequired()])
    email   = StringField("Email", validators=[DataRequired(), Email()])
    submit  = SubmitField("Submit")
