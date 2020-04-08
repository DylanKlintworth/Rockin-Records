from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, FloatField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask_login import current_user
from database.models import *

class SearchForm(FlaskForm):
    search_type = SelectField('Search Options', validators=[DataRequired()],
                              choices=[('albums', 'Album'), ('artists', 'Artist'), ('genres', 'Genre')])
    search_name = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')


class InventoryAccessForm(FlaskForm):
    search_type = SelectField('Inventory Options', validators=[DataRequired()],
                              choices=[('records', 'Records'), ('artists', 'Artists')])
    submit = SubmitField('Alter Inventory')


class UpdateInventoryAccessForm(FlaskForm):
    update_type = SelectField('Update Inventory', validators=[DataRequired()],
                              choices=[('add', 'Add'), ('delete', 'Delete'), ('update', 'Update')])
    submit = SubmitField('Update')


class AddArtistForm(FlaskForm):
    artist_name = StringField('Enter an Artist', validators=[DataRequired()])
    submit = SubmitField('Submit Artist')


class DeleteArtistForm(FlaskForm):
    artists = Artists.query.with_entities(Artists.artist_id, Artists.artist_name).all()
    artist_choices = [(artist[0], artist[1]) for artist in artists]
    artist = SelectField('Select Artist', validators=[DataRequired()], choices=artist_choices, coerce=int)
    submit = SubmitField('Delete the Artist')


class UpdateArtistForm(FlaskForm):
    artists = Artists.query.with_entities(Artists.artist_id, Artists.artist_name).all()
    artist_choices = [(artist[0], artist[1]) for artist in artists]
    artist = SelectField('Select Artist', validators=[DataRequired()], choices=artist_choices, coerce=int)
    artist_name = StringField('Updated Artist Name', validators=[DataRequired()])
    submit = SubmitField('Update the Artist')

    def validate_artist_name(self, artist_name):
        temp = Artists.query.get_or_404(self.artist.data)
        temp_name = temp.artist_name
        if temp_name == artist_name.data:
            raise ValidationError('The name entered is the current Artist name. Please choose a different one.')


class AddRecordForm(FlaskForm):
    artists = Artists.query.with_entities(Artists.artist_id, Artists.artist_name).all()
    artist_choices = [(artist[0], artist[1]) for artist in artists]
    artist = SelectField('Select Artist', validators=[DataRequired()], choices=artist_choices, coerce=int)
    record_name = StringField('Enter Record Name', validators=[DataRequired()])
    record_genre = StringField('Enter Record Genre', validators=[DataRequired()])
    record_price = FloatField('Enter Record Price', validators=[DataRequired()])
    submit = SubmitField('Submit Record')


class DeleteRecordForm(FlaskForm):
    records = Records.query.with_entities(Records.record_id, Records.record_name).all()
    record_choices = [(record[0], (str(record[0]) + " -  " + record[1])) for record in records]
    record = SelectField('Select Record', validators=[DataRequired()], choices=record_choices, coerce=int)
    submit = SubmitField('Delete the Record')


class UpdateRecordForm(FlaskForm):
    records = Records.query.with_entities(Records.record_id, Records.record_name).all()
    record_choices = [(record[0], (str(record[0]) + " - " + record[1])) for record in records]
    record = SelectField('Select Record', validators=[DataRequired()], choices=record_choices, coerce=int)
    submit = SubmitField('Update Record')

class UpdateRecordFormExtended(UpdateRecordForm):
    record = HiddenField("")
    record_name = StringField('Enter Record Name', validators=[DataRequired()])
    record_genre = StringField('Enter Record Genre', validators=[DataRequired()])
    record_price = FloatField('Enter Record Price', validators=[DataRequired()])

class RegistrationForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    street_address = StringField('Street Address')
    city_address = StringField('City')
    state_address = StringField('State')
    zip_code = StringField('Zip Code')
    submit = SubmitField('Update Account Info')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = Users.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
