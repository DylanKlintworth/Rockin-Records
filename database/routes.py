from flask import render_template, url_for, flash, redirect, request, session
from database import app, db, bcrypt
from database.forms import *
from database.models import *
from flask_login import login_user, current_user, logout_user, login_required

rc = None
rec = None

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        flash(f"Search completed for {form.search_name.data}!", 'success')
        if form.search_type.data == 'albums':
            record = f"%{form.search_name.data}%"
            record_list = Records.query.filter(Records.record_name.like(record)).all()
            return render_template('search.html', title='Search Records', form=form, searches=record_list)
    return render_template('search.html', title='Search Records', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Your account has been created! You are now able to login", 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register!', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('account'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.street_address = form.street_address.data
        current_user.city_address = form.city_address.data
        current_user.state_address = form.state_address.data
        current_user.zip_address = form.zip_code.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        redirect(url_for('account'))
    elif request.method == 'GET':
        if current_user == Users.query.get(1):
            return render_template('admin.html', title="Admin Page")
        else:
            form.email.data = current_user.email
            form.street_address.data = current_user.street_address
            form.city_address.data = current_user.city_address
            form.state_address.data = current_user.state_address
            form.zip_code.data = current_user.zip_address
    return render_template('account.html', title='Account', form=form)


@app.route("/inventory_access", methods=['GET', 'POST'])
def inventory_access():
    form = InventoryAccessForm()
    if form.validate_on_submit():
        if form.search_type.data == 'records':
            return redirect(url_for('record_inventory'))
        elif form.search_type.data == 'artists':
            return redirect(url_for('artist_inventory'))
    return render_template('inventory-access.html', title="Inventory Access", form=form)


@app.route("/record_inventory", methods=['GET', 'POST'])
def record_inventory():
    form = UpdateInventoryAccessForm()
    type = 'record_inventory'
    if form.validate_on_submit():
        if form.update_type.data == 'add':
            return redirect(url_for('record_inventory_add'))
        elif form.update_type.data == 'delete':
            return redirect(url_for('record_inventory_delete'))
        elif form.update_type.data == 'update':
            return redirect(url_for('record_inventory_update'))
    return render_template('inventory-update.html', form=form, type=type)


@app.route("/record_inventory_add", methods=['GET', 'POST'])
def record_inventory_add():
    form = AddRecordForm()
    artists = Artists.query.with_entities(Artists.artist_id, Artists.artist_name).all()
    artist_choices = [(artist[0], artist[1]) for artist in artists]
    form.artist.choices = artist_choices
    if form.validate_on_submit():
        record = Records(record_name=form.record_name.data, record_genre=form.record_genre.data, record_price=form.record_price.data, artist_id=form.artist.data)
        db.session.add(record)
        db.session.commit()
        flash('You have submitted an artist!', 'success')
        return redirect(url_for('home'))
    return render_template('record-inventory-add.html', form=form)


@app.route("/record_inventory_delete", methods=['GET', 'POST'])
def record_inventory_delete():
    form = DeleteRecordForm()
    records = Records.query.with_entities(Records.record_id, Records.record_name).all()
    record_choices = [(record[0], (str(record[0]) + " -  " + record[1])) for record in records]
    form.record.choices = record_choices
    if form.validate_on_submit():
        record = Records.query.get_or_404(form.record.data)
        db.session.delete(record)
        db.session.commit()
        flash('You have deleted a record!', 'success')
        return redirect(url_for('home'))
    return render_template('record-inventory-delete.html', form=form)


@app.route("/record_inventory_update", methods=['GET', 'POST'])
def record_inventory_update():
    global rc
    form = UpdateRecordFormArtist()
    artists = Artists.query.with_entities(Artists.artist_id, Artists.artist_name).all()
    artist_choices = [(artist[0], artist[1]) for artist in artists]
    form.artist.choices = artist_choices
    if form.validate_on_submit():
        print('first form')
        artist = Artists.query.get_or_404(form.artist.data)
        if artist:
            artist_id = str(artist.artist_id)
            record_query = db.session.execute(f"SELECT record_id, record_name, record_genre, record_price FROM records WHERE artist_id = {artist_id};").fetchall()
            rc = [(record[0], record[1]) for record in record_query]
            return redirect(url_for('record_inventory_update_record'))
    return render_template('record-inventory-update.html', form=form)


@app.route("/record_inventory_update_record", methods=['GET', 'POST'])
def record_inventory_update_record():
    global rec
    form = UpdateRecordFormRecord()
    form.record.choices = rc
    if form.validate_on_submit():
        record = Records.query.get_or_404(form.record.data)
        if record:
            rec = record
            return redirect(url_for('record_inventory_update_details'))
    return render_template('testing.html', form=form)


@app.route("/record_inventory_update_details", methods=['GET', 'POST'])
def record_inventory_update_details():
    global rec
    print(rec)
    form = UpdateRecordFormDetails()
    if form.validate_on_submit():
        record = rec
        record.record_name = form.record_name.data
        print(record)
        db.session.commit()
        flash('You have updated a record!', 'success')
        return redirect(url_for('home'))
    return render_template('record-inventory-update-details.html', form=form)


@app.route("/artist_inventory", methods=['GET', 'POST'])
def artist_inventory():
    form = UpdateInventoryAccessForm()
    type = 'artist_inventory'
    if form.validate_on_submit():
        if form.update_type.data == 'add':
            return redirect(url_for('artist_inventory_add'))
        elif form.update_type.data == 'delete':
            return redirect(url_for('artist_inventory_delete'))
        elif form.update_type.data == 'update':
            return redirect(url_for('artist_inventory_update'))
    return render_template('inventory-update.html', form=form, type=type)


@app.route("/artist_inventory_add", methods=['GET', 'POST'])
def artist_inventory_add():
    form = AddArtistForm()
    if form.validate_on_submit():
        artist = Artists(artist_name=form.artist_name.data)
        db.session.add(artist)
        db.session.commit()
        flash('You have submitted an artist!', 'success')
        return redirect(url_for('home'))
    return render_template('artist-inventory-add.html', form=form)


@app.route("/artist_inventory_delete", methods=['GET', 'POST'])
def artist_inventory_delete():
    form = DeleteArtistForm()
    artists = Artists.query.with_entities(Artists.artist_id, Artists.artist_name).all()
    artist_choices = [(artist[0], artist[1]) for artist in artists]
    form.artist.choices = artist_choices
    if form.validate_on_submit():
        artist = Artists.query.get_or_404(form.artist.data)
        db.session.delete(artist)
        db.session.commit()
        flash('You have deleted an artist!', 'success')
        return redirect(url_for('home'))
    return render_template('artist-inventory-delete.html', form=form)


@app.route("/artist_inventory_update", methods=['GET', 'POST'])
def artist_inventory_update():
    form = UpdateArtistForm()
    artists = Artists.query.with_entities(Artists.artist_id, Artists.artist_name).all()
    artist_choices = [(artist[0], artist[1]) for artist in artists]
    form.artist.choices = artist_choices
    if form.validate_on_submit():
        artist = Artists.query.get_or_404(form.artist.data)
        artist.artist_name = form.artist_name.data
        db.session.commit()
        flash('You have updated an artist!', 'success')
        return redirect(url_for('home'))
    return render_template('artist-inventory-update.html', form=form)
