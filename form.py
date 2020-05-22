from flask_wtf import FlaskForm
from wtforms import FieldList, Form, FormField, StringField, SubmitField
from wtforms.validators import DataRequired


class CharacterForm(Form):
    char_name = StringField("Character name")
    char_url = StringField("Character icon URL")


class MapForm(FlaskForm):
    map_name = StringField("Map name", validators=[DataRequired()])
    map_base_url = StringField("Map image URL", validators=[DataRequired()])
    characters = FieldList(FormField(CharacterForm), min_entries=10)
    create = SubmitField("Create map!")
