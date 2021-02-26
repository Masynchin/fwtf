from flask import Flask, url_for, request, render_template

app = Flask(__name__)


@app.route("/index/<title>")
def index(title):
    return render_template("index.html", title=title)


@app.route("/training/<prof>")
def training(prof):
    if "инженер" in prof or "строитель" in prof:
        return render_template(
            "training.html",
            photopath=url_for("static", "img/it.png"),
            title="Инженерные тренажеры"
        )
    return render_template(
        "training.html", 
        photopath=url_for("static", "img/ns.png"),
        title="Научные симуляторы"
    )


if __name__ == '__main__':
    app.run(port=5000, debug=True)
