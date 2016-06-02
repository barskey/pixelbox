from flask import render_template, flash, redirect, url_for
from app import app
from .forms import TableForm, SettingsForm
from .models import Img

@app.route('/')
@app.route('/index')
def index():
	user = {'nickname': 'Steve'} # fake user
	return render_template('index.html', title='Home', user=user)
	
@app.route('/table', methods=['GET', 'POST'])
def table():
	form = TableForm()
	return render_template('table.html', title='PixelBox', form=form)

@app.route('/settings', methods=['GET', 'POSt'])
def settings():
    form = SettingsForm()
    return render_template('settings.html', title='Settings', form=form)

@app.route('/images')
def images():
    image_list = [{
            'name': 'test_image' # fake image
        },
        {
            'name': 'image2' # fake image   
        }
    ]
    return render_template('images.html', title='Images', image_list=image_list)

