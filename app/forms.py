from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired


class userLogin(FlaskForm):
	username = StringField('username', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])

class userRegister(FlaskForm):
	username = StringField('username', validators=[DataRequired()])
	email = StringField('email', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])
	passwordConfirm = PasswordField('passwordConfirm', validators=[DataRequired()])
	location = StringField('location', validators=[DataRequired()])

class submitItem(FlaskForm):
	item = StringField('item', validators=[DataRequired()])
	description = TextAreaField('description', validators=[DataRequired()])

class submitItemClaim(FlaskForm):
	yes = SubmitField(label="yes")

class submitItemPossessorUpdate(FlaskForm):
	yes = SubmitField(label="yes")

class confirmDeleteItem(FlaskForm):
	yes = SubmitField(label="yes")