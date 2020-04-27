from flask import render_template, url_for, flash, redirect, request, session
from database import app, db, bcrypt
from database.forms import *
from database.models import *
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        flash(f"Search completed for {form.search_name.data}!", 'success')
        if form.search_type.data == 'albums':
            record = f'"%{form.search_name.data}%"'
            record_list = db.session.execute(f"SELECT records.record_id, records.record_name, \
            records.record_genre, records.record_price \
            FROM records WHERE records.record_name LIKE {record}").fetchall()
            return render_template('search.html', title='Search Records', form=form, searches=record_list,
                                   search_type='albums')
        if form.search_type.data == 'artists':
            artist = f'"%{form.search_name.data}%"'
            artist_list = db.session.execute(f"SELECT artists.artist_id, artists.artist_name \
            FROM artists WHERE artist_name LIKE {artist}").fetchall()
            return render_template('search.html', form=form, searches=artist_list, search_type='artists')
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


@app.route("/record_inventory")
def record_inventory():
    records = Records.query.join(Artists, Records.artist_id == Artists.artist_id) \
        .add_columns(Records.record_id, Records.record_name, Records.record_genre, \
                     Records.record_price, Artists.artist_id, Artists.artist_name).all()
    return render_template('records.html', records=records)


@app.route('/record/<record_id>')
def record(record_id):
    record = Records.query.get_or_404(record_id)
    record_artist = record.query.join(Artists, record.artist_id == Artists.artist_id) \
        .add_columns(Records.record_id, Records.record_name, Records.record_genre, \
                     Records.record_price, Artists.artist_id, Artists.artist_name).filter(Records.record_id == record_id).first()
    return render_template("record.html", record=record_artist)


@app.route('/record/<record_id>/update', methods=['GET', 'POST'])
def update_record(record_id):
    record = Records.query.get_or_404(record_id)
    form = UpdateRecordForm()
    if form.validate_on_submit():
        record.record_name = form.record_name.data
        record.record_genre = form.record_genre.data
        record.record_price = form.record_price.data
        db.session.commit()
        flash('The record has been updated!', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.record_name.data = record.record_name
        form.record_genre.data = record.record_genre
        form.record_price.data = record.record_price
    return render_template('record_update.html', form=form)


@app.route('/record/<record_id>/delete', methods=['GET', 'POST'])
def delete_record(record_id):
    record = Records.query.get_or_404(record_id)
    db.session.delete(record)
    db.session.commit()
    flash('You have deleted a record!', 'success')
    return redirect(url_for('home'))


@app.route('/record/add', methods=['GET', 'POST'])
def add_record():
    form = AddRecordForm()
    if form.validate_on_submit():
        record = Records(artist_id=form.artist.data, record_name=form.record_name.data,
                         record_genre=form.record_genre.data, record_price=form.record_price.data)
        db.session.add(record)
        db.session.commit()
        flash('You have submitted a record!', 'success')
        return redirect(url_for('home'))
    return render_template('record_add.html', form=form)


@app.route('/artists/<artist_id>')
def artists(artist_id):
    artist = Artists.query.get_or_404(artist_id)
    artist_records = db.session.execute(
        f"SELECT artists.artist_id, artists.artist_name, records.record_id, records.record_name, records.record_genre, \
    records.record_price FROM records, artists \
    WHERE (records.artist_id = artists.artist_id) AND (artists.artist_id = {artist.artist_id})"
    ).fetchall()
    return render_template('artist.html', artist_records=artist_records, artist=artist)


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
