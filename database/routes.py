from flask import render_template, url_for, flash, redirect, request, session
from sqlalchemy import and_

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


@app.route('/stores')
def stores():
    stores = Stores.query.all()
    return render_template('stores.html', stores=stores)


@app.route('/store/<store_id>', methods=['GET', 'POST'])
def store(store_id):
    store = Stores.query.get_or_404(store_id)
    store_inventory = Inventory.query.join(Records, Inventory.record_id == Records.record_id)\
    .add_columns(Inventory.quantity, Records.record_id, Records.record_name)\
    .join(Stores, Inventory.store_id == Stores.store_id)\
    .add_columns(Stores.store_id, Stores.store_name).filter(Stores.store_id == Inventory.store_id).all()
    return render_template('store.html', store=store, store_inventory=store_inventory)


@app.route('/employees')
def employees():
    employees = Employees.query.all()
    return render_template('employees.html', employees=employees)


@app.route('/employee/<employee_id>')
def employee(employee_id):
    employee = Employees.query.get_or_404(employee_id)
    return render_template('employee.html', employee=employee)


@app.route('/employee/<employee_id>/delete')
def delete_employee(employee_id):
    employee = Employees.query.get_or_404(employee_id)
    db.session.delete(employee)
    db.session.commit()
    flash(f'You have deleted {employee.first_name + " " + employee.last_name}', 'success')
    return redirect(url_for('home'))


@app.route('/employee/<employee_id>/update', methods=['GET', 'POST'])
def update_employee(employee_id):
    employee = Employees.query.get_or_404(employee_id)
    form = UpdateEmployeeForm()
    if form.validate_on_submit():
        employee.first_name = form.first_name.data
        employee.last_name = form.last_name.data
        employee.birth_date = form.birth_date.data
        employee.street_address = form.street_address.data
        employee.city_address = form.city_address.data
        employee.state_address = form.state_address.data
        employee.zip_address = form.zip_address.data
        employee.phone_number = form.phone_number.data
        employee.job_title = form.job_title.data
        employee.email = form.email.data
        employee.store_id = form.store_id.data
        employee.salary = form.salary.data
        employee.hourly_rate = form.hourly_rate.data
        db.session.commit()
        flash(f'You have updated {employee.first_name + " " + employee.last_name}!', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.first_name.data = employee.first_name
        form.last_name.data = employee.last_name
        form.birth_date.data = employee.birth_date
        form.street_address.data = employee.street_address
        form.city_address.data = employee.city_address
        form.state_address.data = employee.state_address
        form.zip_address.data = employee.zip_address
        form.phone_number.data = employee.phone_number
        form.job_title.data = employee.job_title
        form.email.data = employee.email
        form.store_id.data = employee.store_id
        form.salary.data = employee.salary
        form.hourly_rate.data = employee.hourly_rate
    return render_template('employee_update.html', form=form)


@app.route('/employee/add', methods=['GET', 'POST'])
def add_employee():
    form = AddEmployeeForm()
    if form.validate_on_submit():
        employee = Employees(first_name=form.first_name.data, last_name=form.last_name.data,
                             birth_date=form.birth_date.data, street_address=form.street_address.data,
                             city_address=form.city_address.data, state_address=form.state_address.data,
                             zip_address=form.zip_address.data, phone_number=form.phone_number.data,
                             job_title=form.job_title.data, email=form.email.data,
                             store_id=form.store_id.data,salary=form.salary.data,
                             hourly_rate=form.hourly_rate.data)
        db.session.add(employee)
        db.session.commit()
        flash(f'You have added {employee.first_name + " " + employee.last_name} as an employee!', 'success')
        return redirect(url_for('home'))
    return render_template('employee_add.html', form=form)


@app.route('/inventory/add', methods=['GET', 'POST'])
def add_inventory():
    form = AddInventoryForm()
    if form.validate_on_submit():
        inventory = Inventory(record_id=form.record.data, store_id=form.store.data, quantity=form.quantity.data)
        db.session.add(inventory)
        db.session.commit()
        flash(f'You have added inventory to store #{inventory.store_id}!', 'success')
        return redirect(url_for('home'))
    return render_template('inventory_add.html', form=form)


@app.route('/inventory/<store_id>/<record_id>/update', methods=['GET', 'POST'])
def update_inventory(store_id, record_id):
    inv = Inventory.query.get_or_404([store_id, record_id])
    form = UpdateInventoryForm()
    if form.validate_on_submit():
        inv.quantity = form.quantity.data
        db.session.commit()
        flash('You have updated store inventory!', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.quantity.data = inv.quantity
    return render_template('inventory_update.html', form=form)


@app.route('/inventory/<store_id>/<record_id>', methods=['GET', 'POST'])
def inventory(store_id, record_id):
    inv = Inventory.query.get_or_404([store_id, record_id])
    inventory_join = db.session.execute(
        f'SELECT records.record_id, records.record_name, stores.store_id, stores.store_name,\
            inventory.quantity \
            FROM records, inventory, stores \
            WHERE (inventory.record_id == records.record_id) AND (inventory.store_id == stores.store_id) \
            AND ({inv.store_id} == inventory.store_id) AND ({inv.record_id} == inventory.record_id);'
    ).first()
    return render_template('inventory.html', inventory=inventory_join)


@app.route('/inventory/<store_id>/<record_id>/delete')
def delete_inventory(store_id, record_id):
    inv = Inventory.query.get_or_404([store_id, record_id])
    db.session.delete(inv)
    db.session.commit()
    flash(f'You have deleted inventory for store #{inv.store_id}!', 'success')
    return redirect(url_for('home'))


@app.route('/store/add', methods=['GET', 'POST'])
def add_store():
    form = AddStoreForm()
    if form.validate_on_submit():
        store = Stores(store_name=form.store_name.data, street_address=form.street_address.data, city_address=form.city_address.data, state_address=form.state_address.data, zip_address=form.zip_address.data)
        db.session.add(store)
        db.session.commit()
        flash('You have added a Rockin Records Store!', 'success')
        return redirect(url_for('home'))
    return render_template('store_add.html', form=form)


@app.route('/store/<store_id>/update', methods=['GET', 'POST'])
def update_store(store_id):
    store = Stores.query.get_or_404(store_id)
    form = UpdateStoreForm()
    if form.validate_on_submit():
        store.store_name = form.store_name.data
        store.street_address = form.street_address.data
        store.city_address = form.city_address.data
        store.state_address = form.state_address.data
        store.zip_address = form.zip_address.data
        db.session.commit()
        flash(f'You have updated the Rockin Records {store.store_name} Store!', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.store_name.data = store.store_name
        form.street_address.data = store.street_address
        form.city_address.data = store.city_address
        form.state_address.data = store.state_address
        form.zip_address.data = store.zip_address
    return render_template('store_update.html', form=form)


@app.route('/store/<store_id>/delete')
def delete_store(store_id):
    store = Stores.query.get_or_404(store_id)
    db.session.delete(store)
    db.session.commit()
    flash(f'You have deleted the {store.store_name} store!', 'success')
    return redirect(url_for('home'))


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


@app.route("/orders")
def orders():
   # orders = Orders.query.all()
    orders = Orders.query.join(Users, Orders.user_id == Users.user_id)\
    .add_columns(Orders.order_id, Orders.order_date, Users.email)\
    .join(Stores, Stores.store_id == Orders.store_id)\
    .add_columns(Stores.store_name)
    return render_template('orders.html', orders=orders)


@app.route('/order/add', methods=['GET', 'POST'])
def add_order():
    form = AddOrderForm()
    if form.validate_on_submit():
        order = Orders(user_id=form.user.data, store_id=form.store.data, order_date=form.order_date.data)
        db.session.add(order)
        db.session.commit()
        flash(f'You have submitted an order!', 'success')
        return redirect(url_for('home'))
    return render_template('order_add.html', form=form)


@app.route('/order/<order_id>/delete')
def delete_order(order_id):
    order = Orders.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    flash(f'You have deleted an order!', 'success')
    return redirect(url_for('home'))


@app.route('/order/<order_id>/update', methods=['GET', 'POST'])
def update_order(order_id):
    order = Orders.query.get_or_404(order_id)
    form = UpdateOrderForm()
    if form.validate_on_submit():
        order.order_date = form.order_date.data
        db.session.commit()
        flash('Order Updated!', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.order_date.data = order.order_date
    return render_template('order_update.html', form=form)

@app.route('/order/<order_id>', methods=['GET', 'POST'])
#@app.route('/order')
def order(order_id):
    order = Orders.query.get_or_404(order_id)
    # orders = Orders.query.join(Users, Orders.user_id == Users.user_id)\
    # .add_columns(Orders.order_id, Orders.order_date, Users.email)\
    # .join(Stores, Stores.store_id == Orders.store_id)\
    # .add_columns(Stores.store_name)
    return render_template('order.html', order=order)


@app.route('/recordsales')
def record_sales():
    record_sale_query = RecordSales.query.join(Records, Records.record_id == RecordSales.record_id)\
        .add_columns(Records.record_id, Records.record_name, RecordSales.order_id, RecordSales.quantity)\
        .join(Orders, Orders.order_id == RecordSales.order_id)\
        .add_columns(Orders.order_date, Orders.store_id).all()
    return render_template('record_sales.html', record_sales=record_sale_query)


@app.route('/recordsale/add', methods=['GET', 'POST'])
def add_record_sale():
    form = AddRecordSaleForm()
    if form.validate_on_submit():
        record_sale = RecordSales(record_id=form.record.data, order_id=form.order.data, quantity=form.quantity.data)
        db.session.add(record_sale)
        db.session.commit()
        flash('You have added a record sale!', 'success')
        return redirect(url_for('home'))
    return render_template('record_sale_add.html', form=form)

@app.route('/recordsale/<order_id>/<record_id>/delete')
def delete_record_sale(order_id, record_id):
    record_sale = RecordSales.query.get_or_404([order_id, record_id])
    db.session.delete(record_sale)
    db.session.commit()
    flash('You have deleted a record sale!', 'success')
    return redirect(url_for('home'))


@app.route('/recordsale/<order_id>/<record_id>')
def record_sale(order_id, record_id):
    record_sale = RecordSales.query.get_or_404([order_id, record_id])
    return render_template('record_sale.html', record_sale=record_sale)


@app.route('/recordsale/<order_id>/<record_id>/update', methods=['GET', 'POST'])
def update_record_sale(order_id, record_id):
    record_sale = RecordSales.query.get_or_404([order_id, record_id])
    form = UpdateRecordSaleForm()
    if form.validate_on_submit():
        record_sale.quantity = form.quantity.data
        db.session.commit()
        flash('You have updated a record sale!', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.quantity.data = record_sale.quantity
    return render_template('record_sale_update.html',form=form)

