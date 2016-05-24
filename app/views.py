from flask import render_template, flash, redirect
from app import app
from .forms import TableForm

@app.route('/')
@app.route('/index')
def index():
	user = {'nickname': 'Steve'} # fake user
	return render_template('index.html', title='Home', user=user)
	
@app.route('/table', methods=['GET', 'POST'])
def table():
	form = TableForm()
	return render_template('table.html', title='PixelBox', form=form)