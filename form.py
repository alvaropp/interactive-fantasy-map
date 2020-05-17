from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class CreateMapForm(FlaskForm):
    map_name = StringField("Map name", validators=[DataRequired()])
    map_base_url = StringField("Map base url", validators=[DataRequired()])
    create = SubmitField("Create!")
