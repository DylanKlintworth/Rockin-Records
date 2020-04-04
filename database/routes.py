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
    return render_template('search.html', title='Search Records', form=form)
