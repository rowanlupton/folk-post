from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, SubmitField
from wtforms.validators import DataRequired



class submitItem(FlaskForm):
	item = StringField('item', validators=[DataRequired()])
	description = TextAreaField('description', validators=[DataRequired()])
	name = StringField('name', validators=[DataRequired()])
	location = StringField('location', validators=[DataRequired()])

class submitItemClaim(FlaskForm):
	owner = StringField('owner', validators=[DataRequired()])

class submitItemLocationUpdate(FlaskForm):
	location = StringField('location', validators=[DataRequired()])
	name = StringField('name', validators=[DataRequired()])

class confirmDeleteItem(FlaskForm):
	yes = SubmitField(label="yes")