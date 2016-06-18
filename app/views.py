from flask import render_template, flash, redirect, url_for, session, request, json, jsonify
from PIL import Image
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
		im = Image.new("RGB", (16, 16))
		fp = 'app/static/thumbs/' + newimgname.imgname + '.png'
		im.save(fp)
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
	frame = '1'
	totframes = 1
	form = TableForm()
	if 'imgid' in request.form:
		imgid = request.form['imgid']
		session['imgid'] = imgid
		img = Img.query.get(int(imgid))
		frame = request.form['frame']
		session['frame'] = frame
		pixelarray = Pixel.modelToArray(imgid, frame)
		totframes = Pixel.query.filter_by(img_id = int(imgid)).group_by(Pixel.frame).count()
	elif 'imgid' in session:
		imgid = session['imgid']
		img = Img.query.get(int(imgid))
		frame = session['frame']
		pixelarray = Pixel.modelToArray(imgid, frame)
		totframes = Pixel.query.filter_by(img_id = int(imgid)).group_by(Pixel.frame).count()
	else:
		img = Img(imgname='', animated=False, fps=1)
		pixelarray = [[0 for r in range(16)] for y in range(16)]
	return render_template('table.html', title='PixelBox', form=form, pixels=pixelarray, 
		imgid=imgid, imgname=img.imgname, animated=img.animated, frame=frame, totframes=totframes, fps=img.fps)

@app.route('/update_pixels', methods=['POST'])
def update_pixels():
	animated = False;
	imgid = request.form['imgid']
	session['imgid'] = imgid
	frame = request.form['frame']
	session['frame'] = frame
	try:
		anim = request.form['animated']
		if anim == 'on':
			animated = True
	except:
		aminated = False;
	slider = request.form['fps-slider']
	newname = request.form['imagename']
	img = Img.query.get(int(imgid))
	img.imgname = newname
	img.animated = animated
	img.fps = slider
	db.session.commit()
	im = Image.new("RGB", (16, 16))
	thumb = im.load()	
	items = request.form
	for key, value in items.iteritems():
		if key.startswith('pix_'):
			r, c, h = value.split(',')
			a, row = r.split('=')
			b, col = c.split('=')
			c, hex = h.split('=')
			pixel = Pixel.query.filter_by(img_id=int(imgid), frame=int(frame), row=int(row), col=int(col)).first()
			pixel.hexvalue = hex
			db.session.commit()
			thumb[int(col),int(row)] = (int("0x" + hex[0:2], 0), int("0x" + hex[2:4], 0), int("0x" + hex[4:6], 0))
	fp = 'app/static/thumbs/' + newname + '.png'
	if (int(frame) == 1):
		im.save(fp)
	return json.dumps({'status':'OK'})
	
@app.route('/_get_animation')
def get_animation():
	imgid = request.args.get('imgid', 0, type=int)
	pixels = Pixel.query.filter_by(img_id = imgid).order_by(Pixel.frame)
	test = []
	for pixel in pixels:
		test.append({ "frame": pixel.frame,"row": pixel.row, "col": pixel.col, "hex": pixel.hexvalue})
	return jsonify(pixels = test)

@app.route('/add_frame', methods=['POST'])
def add_frame():
	imgid = request.form['imgid']
	session['imgid'] = imgid
	frame = request.form['frame']
	session['frame'] = int(frame) + 1
	totframes = Pixel.query.filter_by(img_id = imgid).group_by(Pixel.frame).count()
	for i in range (int(frame) + 1, totframes + 1):
		newframe = Pixel.query.filter_by(img_id = int(imgid), frame = i).update(dict(frame=(i + 1)))
		db.session.commit()
	frames = Pixel.query.filter_by(img_id = int(imgid), frame = int(frame))
	for thisframe in frames:
		pixel = Pixel(img_id = int(imgid), frame=int(frame) + 1, row = thisframe.row, col = thisframe.col, hexvalue = thisframe.hexvalue)
		db.session.add(pixel)
	db.session.commit()
	return redirect(url_for('table'))

@app.route('/delete_frame', methods=['POST'])
def delete_frame():
	imgid = request.form['imgid']
	session['imgid'] = imgid
	frame = request.form['frame']
	if int(frame) == 1:
		session['frame'] = 1
	else:
		session['frame'] = int(frame) - 1
	flag = False
	counter = 1
	totframes = Pixel.query.filter_by(img_id = imgid).group_by(Pixel.frame).count()
	for i in range(1, totframes + 1):
		if i == int(frame):
			frames = Pixel.query.filter_by(img_id = int(imgid), frame = i)
			for thisframe in frames:
				db.session.delete(thisframe)
			flag = True
		elif flag:
			newframe = Pixel.query.filter_by(img_id = int(imgid), frame = i).update(dict(frame=(i - 1)))
		counter = counter + 1
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