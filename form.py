import requests
from flask_wtf import FlaskForm
from wtforms import FieldList, Form, FormField, StringField, SubmitField
from wtforms.validators import InputRequired, URL, ValidationError


def url_check(form, field):
    url = field.data
    # If empty, good
    if not url:
        return True
    # Check correct format
    if url and url.split(".")[-1] not in ["jpeg", "jpg", "png"]:
        raise ValidationError("File type must be 'jpeg' or 'png'.")
    # Check website exists
    request = requests.get(url)
    if request.status_code != 200:
        raise ValidationError("The URL provided doesn't seem to exist.")


class CharacterForm(Form):
    char_name = StringField("Character name")
    char_url = StringField("Character icon URL", [url_check])


class MapForm(FlaskForm):
    map_name = StringField("Map name", validators=[InputRequired()])
    map_base_url = StringField(
        "Map image URL", validators=[InputRequired(), url_check]
    )
    characters = FieldList(FormField(CharacterForm), min_entries=10)
    create = SubmitField("Create map!")
