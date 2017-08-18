from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired



class submitItem(FlaskForm):
	item = StringField('item', validators=[DataRequired()])
	description = TextAreaField('description', validators=[DataRequired()])
	name = StringField('name', validators=[DataRequired()])
	location = StringField('location', validators=[DataRequired()])