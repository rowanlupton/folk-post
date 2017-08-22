from app import app, lm
from flask import Flask, render_template, request, session, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from .forms import indexForm, userLogin, userRegister, submitFoundItem, submitLostItem, submitItemClaim, submitItemPossessorUpdate, confirmDeleteItem
from .users import User
from bson.objectid import ObjectId
from flask_pymongo import PyMongo

mongo = PyMongo(app)

@app.route('/', methods=['GET', 'POST'])
def index():
	form=indexForm()
	if form.validate_on_submit():
		field = form.whichField.data
		print(field)
		if field == 'name':
			results = mongo.db.items.find({'item': {'$regex': form.searchQuery.data, '$options': 'i'}})
		elif field == 'description':
			results = mongo.db.items.find({'description': {'$regex': form.searchQuery.data, '$options': 'i'}})
		elif field == 'possessor':
			results = mongo.db.items.find({'possessor': {'$regex': form.searchQuery.data, '$options': 'i'}})
		elif field == 'owner':
			results = mongo.db.items.find({'owner': {'$regex': form.searchQuery.data, '$options': 'i'}})
		elif field == 'currentLocation':
			results = None
		elif field == 'destination':
			results = None
		return render_template('index.html', items=results, mongo=mongo, form=form)
	results = mongo.db.items.find()
	return render_template('index.html', items=results, mongo=mongo, form=form)


@lm.user_loader
def load_user(username):
    u = mongo.db.users.find_one({"_id": username})
    if not u:
        return None
    return User(u['_id'])

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = userLogin()
	if form.validate_on_submit():
		user = mongo.db.users.find_one({'_id': form.username.data})
		if user and User.validate_login(user['password'], form.password.data):
			user_obj = User(user['_id'])
			login_user(user_obj)
			flash("Logged in successfully!", category='success')
			return redirect(request.args.get("next") or url_for('index'))
		else:
			flash('wrong username or password', category='error')
	return render_template('login-page.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def do_register():
	form = userRegister()
	if form.validate_on_submit():
		if form.password.data == form.passwordConfirm.data:
			if mongo.db.users.find({'_id': form.username.data}) == None:
				passwordHash = User.hash_password(form.password.data)
				putData = {'_id': form.username.data, 'name': form.name.data, 'email': form.email.data, 'password' : passwordHash, 'location' : form.location.data}
				mongo.db.users.insert_one(putData)
				return render_template('generic-success.html')
			flash("username taken")
			return render_template('register-page.html', form=form)
		flash("passwords did not match")
		return render_template('register-page.html', form=form)
	return render_template('register-page.html', form=form)

@app.route('/logout')
def do_logout():
	logout_user()
	return redirect(url_for('login'))


@app.route('/found-item', methods=['GET', 'POST'])
@login_required
def foundItemSubmission():
	form = submitFoundItem()
	if form.validate_on_submit():
		putData = {'item' : form.item.data, 'description' : form.description.data, 'possessor' : current_user.username}
		mongo.db.items.insert_one(putData)
		return render_template('api-put-result.html', form=form, putData=putData)
	return render_template('found-item.html', form=form)

@app.route('/lost-item', methods=['GET', 'POST'])
@login_required
def lostItemSubmission():
	form = submitLostItem()
	if form.validate_on_submit():
		putData = {'item' : form.item.data, 'description' : form.description.data, 'owner' : current_user.username}
		mongo.db.items.insert_one(putData)
		return render_template('api-put-result.html', form=form, putData=putData)
	return render_template('lost-item.html', form=form)

@app.route('/user/<name>')
def viewUser(name):
	return render_template('user.html')


@app.route('/location/<location>')
def viewLocation(location):
	return render_template('location.html')


@app.route('/items/<key>')
def viewItem(key):
	result = mongo.db.items.find_one({'_id': ObjectId(key)})
	return render_template('view-item.html', result=result, mongo=mongo)


@app.route('/items/<key>/claim', methods=['GET', 'POST'])
@login_required
def claimItem(key):
	form = submitItemClaim()
	if form.validate_on_submit():
		mongo.db.items.update_one({'_id': ObjectId(key)}, {"$set": {'owner': current_user.username}})
		return render_template('generic-success.html')
	return render_template('claim-item.html', form=form)


@app.route('/items/<key>/update-possessor', methods=['GET', 'POST'])
@login_required
def updateItemPossessor(key):
	form = submitItemPossessorUpdate()
	if form.validate_on_submit():
		mongo.db.items.update_one({'_id': ObjectId(key)}, {"$set": {'possessor': current_user.username}})
		return render_template('generic-success.html')
	return render_template('update-possessor.html', form=form)


@app.route('/items/<key>/delete', methods=['GET', 'POST'])
@login_required
def deleteItem(key):
	form = confirmDeleteItem()
	if form.validate_on_submit():
		mongo.db.items.delete_one({'_id': ObjectId(key)})
		return render_template('generic-success.html')
	return render_template('confirm-delete-item.html', form=form)

