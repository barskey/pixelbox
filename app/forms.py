from flask.ext.wtf import Form
from wtforms import StringField, HiddenField
from wtforms.validators import DataRequired

class TableForm(Form):
    pixValue = HiddenField('pixValue')

class SettingsForm(Form):
    imgduration = StringField('imgduration', default='30', validators=[DataRequired()])

class ImagesForm(Form):
    imgname = StringField('imgname', validators=[DataRequired()])