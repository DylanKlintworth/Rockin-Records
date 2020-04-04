from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class SearchForm(FlaskForm):
    record_name = StringField('Record Search', validators=[DataRequired()])
    submit = SubmitField('Search')
