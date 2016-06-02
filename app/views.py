from flask import render_template, flash, redirect, url_for, session, request, g
from app import app, db
from .forms import TableForm, SettingsForm, ImagesForm
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

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    form = SettingsForm()
    return render_template('settings.html', title='Settings', form=form)

@app.route('/images', methods=['GET', 'POST'])
def images():
    form = ImagesForm()
    image_list = Img.query.all()
    if form.validate_on_submit():
        imgname = Img.make_unique_imgname(form.imgname.data)
        newimg = Img(imgname=imgname, animated=False, fps=0)
        db.session.add(newimg)
        db.session.commit()
        return redirect(url_for('images'))
    return render_template('images.html', title='Images', image_list=image_list, form=form)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500