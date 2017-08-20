from firebase import firebase
from flask import Flask, render_template, request, session, flash
from flask import current_app as current_app
from app.views import userLogin, userRegister, submitItem, submitItemClaim, submitItemPossessorUpdate, confirmDeleteItem
from flask_wtf.csrf import CSRFProtect
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate('./folk-post-firebase-adminsdk-mgffy-1f546500e6.json')
firebase_admin.initialize_app(cred, { 'databaseURL' : 'https://folk-post.firebaseio.com'})

app = Flask(__name__, template_folder='app/templates')
app.config.from_object('config')
#firebase = firebase.FirebaseApplication('https://folk-post.firebaseio.com', None)
from app import views
ref = db.reference('')
items_ref = ref.child('items')
users_ref = ref.child('users')


@app.route('/')
def index():
	results = items_ref.get()
	return render_template('index.html', results=results)


@app.route('/login', methods=['GET', 'POST'])
def do_login():
	form = userLogin()
	if form.validate_on_submit():
		if users_ref.child(form.username.data).child('password').get() == form.password.data:
			session['logged_in'] = True
			return index()
		else:
			flash('wrong password')

	return render_template('login-page.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def do_register():
	form = userRegister()
	if form.validate_on_submit():
		if form.password.data == form.passwordConfirm.data:
			putData = {'password' : form.password.data, 'location' : form.location.data}
			users_ref.child(form.username.data).set(putData)
			return render_template('generic-success.html')
		return "passwords did not match"
	return render_template('register-page.html', form=form)


@app.route('/submission', methods=['GET', 'POST'])
def itemSubmission():
	form = submitItem()
	if form.validate_on_submit():
		putData = {'item' : form.item.data, 'description' : form.description.data, 'possessor' : form.possessor.data, 'location' : form.location.data}
		items_ref.push(putData)
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
	result = items_ref.child(key).get()
	return render_template('view-item.html', result=result)


@app.route('/items/<key>/claim', methods=['GET', 'POST'])
def claimItem(key):
	form = submitItemClaim()
	if form.validate_on_submit():
		items_ref.child(key).child('owner').set(form.owner.data)
		return render_template('generic-success.html')
	return render_template('claim-item.html', form=form)


@app.route('/<possessor>/<item>/update-possessor', methods=['GET', 'POST'])
def updateItemPossessor(possessor, item):
	form = submitItemPossessorUpdate()
	if form.validate_on_submit():
		putData = {'possessor' : form.possessor.data}
		items_ref.child(item).update(putData)
		return render_template('generic-success.html')
	return render_template('update-possessor.html', form=form)


@app.route('/items/<item>/delete', methods=['GET', 'POST'])
def deleteItem(item):
	form = confirmDeleteItem()
	if form.validate_on_submit():
		items_ref.child(item).delete()
		return render_template('generic-success.html')
	return render_template('confirm-delete-item.html', form=form)

