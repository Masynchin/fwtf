import json
from pathlib import Path

from flask import url_for, render_template, redirect, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash

from app import app, db
from app.forms import *
from app.models import *


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

        user = User.get_by_email(email)
        if user is not None:
            flash("Email is already taken")
            return render_template("register.html", form=form)

        user = User(
            email=email, hashed_password=password, surname=surname, name=name,
            age=age, position=position, speciality=speciality
        )
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)

        return redirect("/")

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template("login.html",
            message="Неправильный логин или пароль", form=form)

    return render_template("login.html", title="Авторизация", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_required
@app.route("/addjob", methods=["GET", "POST"])
def addjob():
    form = JobForm()
    if form.validate_on_submit():
        team_leader = form.team_leader.data
        collaborators = form.collaborators.data
        for worker_id in [team_leader, *map(int, collaborators.split(","))]:
            worker = User.query.get(worker_id)
            if worker is None:
                flash("Incorrect team_leader or collaborator ID")
                return render_template("addjob.html", form=form)

        job = Jobs(
            team_leader=team_leader,
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=collaborators,
            is_finished=form.is_finished.data
        )
        db.session.add(job)
        db.session.commit()

        return redirect("/")

    return render_template("addjob.html", form=form)


@app.route("/editjob/<int:job_id>", methods=["GET", "POST"])
def editjob(job_id):
    job = Jobs.query.get(job_id)
    form = JobForm()
    if form.validate_on_submit():
        if (
            current_user.is_authenticated and
            current_user.id in (job.team_lead.id, 1)
            and job is not None
        ):
            team_leader = form.team_leader.data
            collaborators = form.collaborators.data
            for worker_id in [team_leader, *map(int, collaborators.split(","))]:
                worker = User.query.get(worker_id)
                if worker is None:
                    flash("Incorrect team_leader or collaborator ID")
                    return render_template("editjob.html", form=form)

            job.team_leader = team_leader
            job.job = form.job.data
            job.work_size = form.work_size.data
            job.collaborators = collaborators
            job.is_finished = form.is_finished.data
            db.session.commit()
            return redirect("/")
        else:
            flash("Not enough rights for that action")
            return redirect("/")

    if (
        current_user.is_authenticated and
        current_user.id in (job.team_lead.id, 1)
        and job is not None
    ):
        return render_template("addjob.html", form=form)
    else:
        flash("Not enough rights for that action")
        return redirect("/")


@app.route("/deljob/<int:job_id>")
def deljob(job_id):
    job = Jobs.query.get(job_id)
    if (
        current_user.is_authenticated and
        current_user.id in (job.team_lead.id, 1)
    ):
        db.session.delete(job)
        db.session.commit()
        flash("Succecsfully delete")
    return redirect("/")
