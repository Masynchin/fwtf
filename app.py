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


if __name__ == '__main__':
    app.run(port=5000, debug=True)
