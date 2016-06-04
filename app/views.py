from flask import render_template, flash, redirect, url_for, session, request, g
from app import app, db
from .forms import TableForm, SettingsForm, ImagesForm
from .models import Img, Pixel

@app.route('/')
@app.route('/index')
def index():
	user = {'nickname': 'Steve'} # fake user
	return render_template('index.html', title='Home', user=user)
	
@app.route('/table', methods=['GET', 'POST'])
def table():
	errors = []
	results = {}
	form = TableForm()
	if 'imgid' in request.args:
		imgid = request.args['imgid']
		img = Img.query.get(int(imgid))
		pixels = Pixel.query.filter_by(img_id = int(img.id)).order_by(Pixel.row).order_by(Pixel.col)
		pixelarray = [[0 for r in range(16)] for y in range(16)]
		for pixel in pixels:
			pixelarray[pixel.row][pixel.col] = pixel.hexvalue
	else:
		pixelarray = [[0 for r in range(16)] for y in range(16)]
	return render_template('table.html', title='PixelBox', form=form, img='', pixels=pixelarray)

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
		img = Img(imgname = imgname, animated = False, fps = 0)
		db.session.add(img)
		db.session.commit()
		newimgname = Img.query.filter_by(imgname=imgname).first_or_404()
		newimgid = newimgname.id
		for r in range (16):
			for c in range (16):
				pixel = Pixel(img_id = newimgid, row = r, col = c, hexvalue = '000000')
				db.session.add(pixel)
		db.session.commit()
		return redirect(url_for('images'))
	return render_template('images.html', title='Images', image_list=image_list, form=form)

@app.route('/delete_image', methods=['GET'])
def delete_image():
	imgid = request.args['imgid']
	img = Img.query.get(int(imgid))
	db.session.delete(img)
	db.session.commit()
	return redirect(url_for('images'))

@app.errorhandler(404)
def not_found_error(error):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
	db.session.rollback()
	return render_template('500.html'), 500