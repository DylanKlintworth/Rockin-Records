from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, FloatField, DateField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from flask_login import current_user
from database.models import *
from database.routes import *
from database import db


class AddToCart(FlaskForm):
    stores = Stores.query.with_entities(Stores.store_id, Stores.store_name).all()
    store_choices = [(store[0], store[1]) for store in stores]
    store = SelectField('Store', choices=store_choices, validators=[DataRequired()], coerce=int)
    quantity = IntegerField('Quantity:', validators=[DataRequired()])
    submit = SubmitField('Add Record to Cart')

    def __init__(self):
        super(AddToCart, self).__init__()
        stores = Stores.query.with_entities(Stores.store_id, Stores.store_name).all()
        store_choices = [(store[0], store[1]) for store in stores]
        self.store.choices = store_choices


class CheckOutForm(FlaskForm):
    submit = SubmitField('Checkout!')




class SearchForm(FlaskForm):
    search_type = SelectField('Search Options', validators=[DataRequired()],
                              choices=[('albums', 'Album'), ('artists', 'Artist')])
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


class AddStoreForm(FlaskForm):
    store_name = StringField('Store Name:', validators=[DataRequired()])
    street_address = StringField('Street Address:', validators=[DataRequired()])
    city_address = StringField('City:', validators=[DataRequired()])
    state_address = StringField('State:', validators=[DataRequired(), Length(2, 2)])
    zip_address = StringField('Zip Code:', validators=[DataRequired(), Length(5, 5)])
    submit = SubmitField('Add Store')


class UpdateStoreForm(AddStoreForm):
    submit = SubmitField('Update Store')
    
    def __init__(self):
        super(UpdateStoreForm, self).__init__()


class AddEmployeeForm(FlaskForm):
    stores = Stores.query.with_entities(Stores.store_id, Stores.store_name)
    store_choices = [(store[0], store[1]) for store in stores]
    first_name = StringField('First Name:', validators=[DataRequired()])
    last_name = StringField('Last Name:', validators=[DataRequired()])
    birth_date = DateField('Birthdate:', validators=[DataRequired()])
    street_address = StringField('Street Address:', validators=[DataRequired()])
    city_address = StringField('City:', validators=[DataRequired()])
    state_address = StringField('State:', validators=[DataRequired(), Length(2, 2)])
    zip_address = StringField('Zip Code:', validators=[DataRequired(), Length(5, 5)])
    phone_number = StringField('Phone Number:', validators=[DataRequired()])
    job_title = StringField('Job Title:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    store_id = SelectField('Store:', validators=[DataRequired()], choices=store_choices, coerce=int)
    salary = FloatField('Salary:')
    hourly_rate = FloatField('Hourly Rate:')
    submit = SubmitField('Add an Employee')

    def __init__(self, *args, **kwargs):
        super(AddEmployeeForm, self).__init__()
        stores = Stores.query.with_entities(Stores.store_id, Stores.store_name)
        store_choices = [(store[0], store[1]) for store in stores]
        self.store_id.choices = store_choices


class UpdateEmployeeForm(AddEmployeeForm):
    submit = SubmitField('Update Employee')
    
    def __init__(self):
        super(UpdateEmployeeForm, self).__init__()


class AddInventoryForm(FlaskForm):
    records = Records.query.with_entities(Records.record_id, Records.record_name).all()
    record_choices = [(record[0], (str(record[0]) + " -  " + record[1])) for record in records]
    stores = Stores.query.with_entities(Stores.store_id, Stores.store_name).all()
    store_choices = [(store[0], store[1]) for store in stores]
    record = SelectField('Record:', choices=record_choices, coerce=int, validators=[DataRequired()])
    store = SelectField('Store:', choices=store_choices, coerce=int, validators=[DataRequired()])
    quantity = IntegerField('Record Quantity:', validators=[DataRequired()])
    submit = SubmitField('Add Inventory')

    def __init__(self, *args, **kwargs):
        super(AddInventoryForm, self).__init__()
        records = Records.query.with_entities(Records.record_id, Records.record_name).all()
        record_choices = [(record[0], (str(record[0]) + " -  " + record[1])) for record in records]
        stores = Stores.query.with_entities(Stores.store_id, Stores.store_name).all()
        store_choices = [(store[0], store[1]) for store in stores]
        self.record.choices = record_choices
        self.store.choices = store_choices


class UpdateInventoryForm(AddInventoryForm):
    record = HiddenField('')
    store = HiddenField('')
    submit = SubmitField('Update Inventory')


class DeleteArtistForm(FlaskForm):
    artists = Artists.query.with_entities(Artists.artist_id, Artists.artist_name).all()
    artist_choices = [(artist[0], artist[1]) for artist in artists]
    artist = SelectField('Select Artist', validators=[DataRequired()], choices=artist_choices, coerce=int)
    submit = SubmitField('Delete the Artist')

    def __init__(self, *args, **kwargs):
        super(DeleteArtistForm, self).__init__()
        artists = Artists.query.with_entities(Artists.artist_id, Artists.artist_name).all()
        artist_choices = [(artist[0], artist[1]) for artist in artists]
        self.artist.choices = artist_choices


class UpdateArtistForm(FlaskForm):
    artists = Artists.query.with_entities(Artists.artist_id, Artists.artist_name).all()
    artist_choices = [(artist[0], artist[1]) for artist in artists]
    artist = SelectField('Select Artist', validators=[DataRequired()], choices=artist_choices, coerce=int)
    artist_name = StringField('Updated Artist Name', validators=[DataRequired()])
    submit = SubmitField('Update the Artist')

    def __init__(self, *args, **kwargs):
        super(UpdateArtistForm, self).__init__()
        artists = Artists.query.with_entities(Artists.artist_id, Artists.artist_name).all()
        artist_choices = [(artist[0], artist[1]) for artist in artists]
        self.artist.choices = artist_choices

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

    def __init__(self, *args, **kwargs):
        super(AddRecordForm, self).__init__()
        artists = Artists.query.with_entities(Artists.artist_id, Artists.artist_name).all()
        artist_choices = [(artist[0], artist[1]) for artist in artists]
        self.artist.choices = artist_choices


class DeleteRecordForm(FlaskForm):
    records = Records.query.with_entities(Records.record_id, Records.record_name).all()
    record_choices = [(record[0], (str(record[0]) + " -  " + record[1])) for record in records]
    record = SelectField('Select Record', validators=[DataRequired()], choices=record_choices, coerce=int)
    submit = SubmitField('Delete the Record')


class UpdateRecordForm(FlaskForm):
    record_name = StringField('Record Name:', validators=[DataRequired()])
    record_genre = StringField('Record Genre:', validators=[DataRequired()])
    record_price = FloatField('Record Price:', validators=[DataRequired()])
    submit = SubmitField('Update the Record')


class AddOrderForm(FlaskForm):
    users = Users.query.with_entities(Users.user_id, Users.email).all()
    user_choices = [(user[0], user[1]) for user in users]
    stores = Stores.query.with_entities(Stores.store_id, Stores.store_name).all()
    store_choices = [(store[0], store[1]) for store in stores]
    order_date = DateField('Order Date (YYYY-MM-DD):', validators=[DataRequired()])
    user = SelectField('User:', validators=[DataRequired()], choices=user_choices, coerce=int)
    store = SelectField('Store:', validators=[DataRequired()], choices=store_choices, coerce=int)
    submit = SubmitField('Add Order')

    def __init__(self, *args, **kwargs):
        super(AddOrderForm, self).__init__()
        users = Users.query.with_entities(Users.user_id, Users.email).all()
        user_choices = [(user[0], user[1]) for user in users]
        stores = Stores.query.with_entities(Stores.store_id, Stores.store_name).all()
        store_choices = [(store[0], store[1]) for store in stores]
        self.store.choices = store_choices
        self.user.choices = user_choices


class UpdateOrderForm(AddOrderForm):
    user = HiddenField('')
    store = HiddenField('')
    submit = SubmitField('Update Order')


class AddRecordSaleForm(FlaskForm):
    orders = Orders.query.with_entities(Orders.order_id).all()
    order_choices = [(order[0], order[0]) for order in orders]
    records = Records.query.with_entities(Records.record_id, Records.record_name).all()
    record_choices = [(record[0], record[1]) for record in records]
    order = SelectField('Order:', choices=order_choices, validators=[DataRequired()], coerce=int)
    record = SelectField('Record:', choices=record_choices, validators=[DataRequired()], coerce=int)
    quantity = IntegerField('Quantity:', validators=[DataRequired()])
    submit = SubmitField('Add Record Sale')
    
    def __init__(self, *args, **kwargs):
        super(AddRecordSaleForm, self).__init__()
        orders = Orders.query.with_entities(Orders.order_id).all()
        order_choices = [(order[0], order[0]) for order in orders]
        records = Records.query.with_entities(Records.record_id, Records.record_name).all()
        record_choices = [(record[0], record[1]) for record in records]
        self.order.choices = order_choices
        self.record.choices = record_choices


class UpdateRecordSaleForm(AddRecordSaleForm):
    order = HiddenField('')
    record = HiddenField('')
    submit = SubmitField('Update Record Sale')


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
    email = StringField('Email', validators=[DataRequired(), Email()])
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
