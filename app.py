from flask import Flask, render_template, flash, redirect
from form import CreateMapForm
from process_new_map import process_form


app = Flask(__name__)
with open("secret.txt", "r") as secret_f:
    app.config["SECRET_KEY"] = secret_f.read()


@app.route("/", methods=["GET", "POST"])
def home():
    form = CreateMapForm()
    if form.validate_on_submit():
        text = process_form(form)
        flash(text)
    return render_template("index.html", title="Create a new map", form=form)


if __name__ == "__main__":
    app.run(debug=True)