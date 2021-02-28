import json
from pathlib import Path

from flask import url_for, render_template, redirect
from werkzeug.security import generate_password_hash

from app import app, db
from app.forms import LoginForm, ImageForm, RegisterForm
from app.models import User, Jobs


@app.route("/index/<title>")
def index(title):
    return render_template("index.html", title=title)


@app.route("/training/<prof>")
def training(prof):
    if "инженер" in prof or "строитель" in prof:
        title="Инженерные тренажеры"
        image_path = url_for("static", filename="img/engineer.jpg")
    else:
        title="Научные симуляторы"
        image_path = url_for("static", filename="img/science.jpg")
    return render_template("training.html", title=title, image_path=image_path)


@app.route("/list_prof/<list_type>")
def list_prof(list_type):
    if list_type in ("ol", "ul"):
        return render_template("list_prof.html", list_type=list_type,
            proffs=[
                "инженер-исследователь",
                "пилот",
                "строитель",
                "экзобиолог",
                "врач",
                "инженер по терраформированию",
                "климатолог",
                "специалист по радиационной защите",
                "астролог",
        ])
    else:
        return render_template("error.html", desc="Incorrect list_type param")


@app.route("/answer")
@app.route("/auto_answer")
def auto_answer():
    return render_template("auto_answer.html", fields={
        "Фамилия": "Watny",
        "Имя": "Mark",
        "Образование": "наивысшее",
        "Профессия": "штурман марсохода",
        "Пол": "male",
        "Мотивация": "Всегда мечтал застрять на Марсе!",
        "Готовы остаться на Марсе?": True,
    })


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect("/index/starter")
    return render_template("login.html", title="Авторизация", form=form)


@app.route("/distribution")
def distribution():
    return render_template("distribution.html", persons=[
        "Улов Налимов", "Рекорд Надоев", "Рулон Обоев", "Учёт Расходов",
        "Облом Пиндосов", "Камаз Отходов", "Парад Уродов",
    ])


@app.route("/table/<sex>/<int:age>")
def table(sex, age):
    filename = "img/adult.png" if age >= 21 else "img/baby.png"
    if sex == "male":
        color = "#00f" if age >= 21 else "#88f"
    elif sex == "female":
        color = "#f00" if age >= 21 else "#f88"
    return render_template("table.html", color=color,
        filename=url_for("static", filename=filename))


@app.route("/galery", methods=["GET", "POST"])
def galery():
    form = ImageForm()
    if form.validate_on_submit():
        image = form.image.data
        image.save(Path(f"static/img/carousel/{image.filename}"))
        return redirect("/galery")

    images = [url_for("static", filename=f"img/carousel/{name}")
        for name in _get_images()]
    return render_template("galery.html", images=images, form=form)


def _get_images():
    return [image.name for image in Path("app/static/img/carousel").iterdir()]


@app.route("/member")
def member():
    with open("app/templates/member.json", encoding="u8") as f:
        member = json.load(f)
    return render_template("member.html", member=member)


@app.route("/")
def works_log():
    jobs = Jobs.query.all()
    return render_template("works_log.html", jobs=jobs)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        password = generate_password_hash(form.password.data)
        surname = form.surname.data
        name = form.name.data
        age = form.age.data
        address = form.address.data
        position = form.position.data
        speciality = form.speciality.data

        user = User(
            email=email, hashed_password=password, surname=surname, name=name,
            age=age, position=position, speciality=speciality
        )
        db.session.add(user)
        db.session.commit()

        return redirect("/index/starter")

    return render_template("register.html", form=form)
