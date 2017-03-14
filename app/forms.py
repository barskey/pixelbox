from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField
from wtforms.validators import DataRequired

class TableForm(FlaskForm):
    imgid = HiddenField('imgid')
    frame = HiddenField('frame')

class SettingsForm(FlaskForm):
    imgduration = StringField('imgduration', default='30', validators=[DataRequired()])

class ImagesForm(FlaskForm):
    imgname = StringField('imgname', validators=[DataRequired()])