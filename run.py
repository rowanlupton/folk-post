import os
from flask import Flask, render_template, request, session, flash
from flask import current_app as current_app
from app.views import userLogin, userRegister, submitItem, submitItemClaim, submitItemPossessorUpdate, confirmDeleteItem
from flask_wtf.csrf import CSRFProtect
import flask_login
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__, template_folder='app/templates')
app.config.from_object('config')

uri = 'mongodb://folk-post:'+os.environ['mongodb-password']+'@folk-post-shard-00-00-jwcpw.mongodb.net:27017,folk-post-shard-00-01-jwcpw.mongodb.net:27017,folk-post-shard-00-02-jwcpw.mongodb.net:27017/<DATABASE>?ssl=true&replicaSet=folk-post-shard-0&authSource=admin'
app.config['MONGO_URI'] = uri
mongo = PyMongo(app, 'MONGO')


# your regularly scheduled app
@app.route('/')
def index():
	results = mongo.db.items.find()
	return render_template('index.html', items=results)


# @app.route('/login', methods=['GET', 'POST'])
# def do_login():
# 	form = userLogin()
# 	if form.validate_on_submit():
# 		if users_ref.child(form.username.data).child('password').get() == form.password.data:
# 			flask_login.login_user()
# 			return index()
# 		else:
# 			flash('wrong password')

# 	return render_template('login-page.html', form=form)

# @app.route('/register', methods=['GET', 'POST'])
# def do_register():
# 	form = userRegister()
# 	if form.validate_on_submit():
# 		if form.password.data == form.passwordConfirm.data:
# 			putData = {'password' : form.password.data, 'location' : form.location.data}
# 			users_ref.child(form.username.data).set(putData)
# 			return render_template('generic-success.html')
# 		return "passwords did not match"
# 	return render_template('register-page.html', form=form)


@app.route('/submission', methods=['GET', 'POST'])
# @flask_login.login_required
def itemSubmission():
	form = submitItem()
	if form.validate_on_submit():
		putData = {'item' : form.item.data, 'description' : form.description.data, 'possessor' : form.possessor.data, 'location' : form.location.data}
		mongo.db.items.insert_one(putData)
		return render_template('api-put-result.html', form=form, putData=putData)
	return render_template('submit-item.html', form=form)


@app.route('/user/<name>')
def viewUser(name):
	return render_template('user.html')


@app.route('/location/<location>')
def viewLocation(location):
	return render_template('location.html')


@app.route('/items/<key>')
def viewItem(key):
	result = mongo.db.items.find_one({'_id': ObjectId(key)})
	return render_template('view-item.html', result=result)


@app.route('/items/<key>/claim', methods=['GET', 'POST'])
def claimItem(key):
	form = submitItemClaim()
	if form.validate_on_submit():
		mongo.db.items.update_one({'_id': ObjectId(key)}, {"$set": {'owner': form.owner.data}})
		return render_template('generic-success.html')
	return render_template('claim-item.html', form=form)


@app.route('/items/<key>/update-possessor', methods=['GET', 'POST'])
def updateItemPossessor(key):
	form = submitItemPossessorUpdate()
	if form.validate_on_submit():
		putData = {'possessor' : form.possessor.data}
		mongo.db.items.update_one({'_id': ObjectId(key)}, {"$set": {'possessor': form.possessor.data}})
		return render_template('generic-success.html')
	return render_template('update-possessor.html', form=form)


@app.route('/items/<key>/delete', methods=['GET', 'POST'])
def deleteItem(key):
	form = confirmDeleteItem()
	if form.validate_on_submit():
		mongo.db.items.delete_one({'_id': ObjectId(key)})
		return render_template('generic-success.html')
	return render_template('confirm-delete-item.html', form=form)

