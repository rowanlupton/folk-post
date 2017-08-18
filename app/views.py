from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired


class userLogin(FlaskForm):
	username = StringField('username', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])

class userRegister(FlaskForm):
	username = StringField('username', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])
	passwordConfirm = PasswordField('passwordConfirm', validators=[DataRequired()])
	#location = StringField('location', validators=[DataRequired()])

class submitItem(FlaskForm):
	item = StringField('item', validators=[DataRequired()])
	description = TextAreaField('description', validators=[DataRequired()])
	possessor = StringField('possessor', validators=[DataRequired()])
	location = StringField('location', validators=[DataRequired()])

class submitItemClaim(FlaskForm):
	owner = StringField('owner', validators=[DataRequired()])

class submitItemLocationUpdate(FlaskForm):
	location = StringField('location', validators=[DataRequired()])
	possessor = StringField('possessor', validators=[DataRequired()])

class confirmDeleteItem(FlaskForm):
	yes = SubmitField(label="yes")