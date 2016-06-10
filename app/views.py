from flask import render_template, flash, redirect, url_for, session, request, g
from app import app, db
from .forms import TableForm, SettingsForm, ImagesForm
from .models import Img, Pixel

@app.route('/')
@app.route('/index')
def index():
	user = {'nickname': 'Steve'} # fake user
	return render_template('index.html', title='Home', user=user)
	
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
				pixel = Pixel(img_id = newimgid, frame=1, row = r, col = c, hexvalue = '000000')
				db.session.add(pixel)
		db.session.commit()
		return redirect(url_for('images'))
	return render_template('images.html', title='Images', image_list=image_list, form=form)

@app.route('/delete_image', methods=['GET'])
def delete_image():
	imgid = int(request.args['imgid'])
	img = Img.query.get(imgid)
	db.session.delete(img)
	db.session.commit()
	return redirect(url_for('images'))
	
@app.route('/table', methods=['GET', 'POST'])
def table():
	imgid = None
	img = None
	form = TableForm()
	if 'imgid' in request.form:
		imgid = request.form['imgid']
		session['imgid'] = imgid
		img = Img.query.get(int(imgid))
		pixelarray = Pixel.modelToArray(imgid)
	elif 'imgid' in session:
		imgid = session['imgid']
		img = Img.query.get(int(imgid))
		pixelarray = Pixel.modelToArray(imgid)
	else:
		img = Img(imgname='', animated=False, fps=0)
		pixelarray = [[0 for r in range(16)] for y in range(16)]
	return render_template('table.html', title='PixelBox', form=form, pixels=pixelarray, 
		imgid=imgid, imgname=img.imgname, animated=img.animated)

@app.route('/update_pixels', methods=['POST'])
def update_pixels():
	imgid = None
	animated = False;
	try:
		imgid = request.form['imgid']
		session['imgid'] = imgid
	except LookupError:
		return render_template('404.html')
	try:
		anim = request.form['animated']
		if anim == 'on':
			animated = True
	except:
		animated = False;
	newname = request.form['imagename']
	img = Img.query.get(int(imgid))
	img.imgname = newname
	img.animated = animated
	db.session.commit()
	items = request.form
	for key, value in items.iteritems():
		if key.startswith('pix_'):
			r, c, h = value.split(",")
			a, row = r.split("=")
			b, col = c.split("=")
			c, hex = h.split("=")
			pixel = Pixel.query.filter_by(row=row, col=col, img_id=int(imgid)).first()
			pixel.hexvalue = hex
			db.session.commit() 
	return redirect(url_for('table'))

@app.route('/testpost', methods=['POST'])
def testpost():
	items = request.form
	return render_template('testpost.html', items=items)

@app.errorhandler(404)
def not_found_error(error):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
	db.session.rollback()
	return render_template('500.html'), 500