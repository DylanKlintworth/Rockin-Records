from flask import render_template, url_for, flash, redirect, request, abort
from database import app, db
from database.forms import SearchForm


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
