from flask import Flask, url_for, request, render_template

app = Flask(__name__)


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


if __name__ == '__main__':
    app.run(port=5000, debug=True)
