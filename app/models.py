from app import db

class Img(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	imgname = db.Column(db.String(64), index=True, unique=True)
	animated = db.Column(db.Boolean)
	fps = db.Column(db.Integer)
	pixels = db.relationship('Pixel', backref='pic', lazy='dynamic')
            
	def __repr__(self):
		return '<Image %r>' % (self.imgname)

class Pixel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	img_id = db.Column(db.Integer, db.ForeignKey('img.id'))
	row = db.Column(db.Integer)
	col= db.Column(db.Integer)
	hexvalue = db.Column(db.String(6))
	
	def __repr__(self):
		return '<Pixel r:%ic:%i %r>' % (self.row, self.col, self.hexvalue)
