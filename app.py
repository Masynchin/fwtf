import secrets

from flask import Flask, url_for, request, render_template, redirect

from forms import LoginForm


app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_urlsafe(16)


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


if __name__ == '__main__':
    app.run(port=5000, debug=True)
