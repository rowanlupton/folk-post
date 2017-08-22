from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired


class indexForm(FlaskForm):
	fieldChoices = [('name','name'),('description','description'),('possessor','possessor'),('owner','owner'),('currentLocation','current location'),('destination','destination')]
	whichField = SelectField('field', choices = fieldChoices, validators=[DataRequired()])
	searchQuery = StringField('query', validators=[DataRequired()])
	filterButton = SubmitField('filter', validators=[DataRequired()])


class userLogin(FlaskForm):
	username = StringField('username', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])

class userRegister(FlaskForm):
	username = StringField('username', validators=[DataRequired()])
	name = StringField('name', validators=[DataRequired()])
	email = StringField('email', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])
	passwordConfirm = PasswordField('passwordConfirm', validators=[DataRequired()])
	location = StringField('location', validators=[DataRequired()])

class submitLostItem(FlaskForm):
	item = StringField('item', validators=[DataRequired()])
	description = TextAreaField('description', validators=[DataRequired()])

class submitFoundItem(FlaskForm):
	item = StringField('item', validators=[DataRequired()])
	description = TextAreaField('description', validators=[DataRequired()])

class submitItemClaim(FlaskForm):
	yes = SubmitField(label="yes")

class submitItemPossessorUpdate(FlaskForm):
	yes = SubmitField(label="yes")

class confirmDeleteItem(FlaskForm):
	yes = SubmitField(label="yes")