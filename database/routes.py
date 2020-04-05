from flask import render_template, url_for, flash, redirect, request
from database import app, db, bcrypt
from database.forms import SearchForm, RegistrationForm, LoginForm, UpdateAccountForm
from database.models import *
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        flash(f"Search completed for {form.record_name.data}!", 'success')
        return redirect(url_for('home'))
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
            return redirect(next_page) if next_page else redirect(url_for('home'))
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
        form.email.data = current_user.email
        form.street_address.data = current_user.street_address
        form.city_address.data = current_user.city_address
        form.state_address.data = current_user.state_address
        form.zip_code.data = current_user.zip_address
    return render_template('account.html', title='Account', form=form)