from flask_wtf import FlaskForm
from wtforms import SearchField, validators

class CiudadForm(FlaskForm):
    ciudad = SearchField(validators=[validators.DataRequired()])