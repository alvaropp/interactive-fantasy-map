from flask import flash, Flask, Markup, render_template, redirect, request
from form import MapForm
from process_new_map import create_map_from_form


app = Flask(__name__)

with open("secret.txt", "r") as secret_f:
    app.config["SECRET_KEY"] = secret_f.read()


@app.route("/", methods=["GET", "POST"])
def home():
    form = MapForm()
    if form.validate_on_submit():
        map_website_path = create_map_from_form(form)
        map_name = map_website_path.split("/")[-1].split(".")[0]
        full_url = f"{request.base_url}maps/" + map_website_path
        flash(Markup(f"Map created successfully: <a href={full_url}>{map_name}</a>"))

    return render_template("index.html", title="Create a new map", form=form)


@app.route("/maps/<map_uuid>/<map_name>.html")
def show_map(map_uuid, map_name):
    return render_template(f"map_template.html", data=[map_uuid, map_name])


if __name__ == "__main__":
    app.run(debug=True)
