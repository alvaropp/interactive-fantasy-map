from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CreateMapForm(FlaskForm):
    map_name = StringField("Map name", validators=[DataRequired()])
    map_base_url = StringField("Map image URL", validators=[DataRequired()])
    char_name_1 = StringField("Character 1 name", validators=[DataRequired()])
    char_name_2 = StringField("Character 2 name", validators=[DataRequired()])
    char_name_3 = StringField("Character 3 name", validators=[DataRequired()])
    char_icon_1 = StringField("Character 1 icon", validators=[DataRequired()])
    char_icon_2 = StringField("Character 2 icon", validators=[DataRequired()])
    char_icon_3 = StringField("Character 3 icon", validators=[DataRequired()])
    create = SubmitField("Create map!")
