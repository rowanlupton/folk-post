from firebase import firebase
from flask import Flask, render_template, request, session
from flask import current_app as current_app
from app.views import submitItem
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__, template_folder='app/templates')
app.config.from_object('config')
firebase = firebase.FirebaseApplication('https://folk-post.firebaseio.com', None)
from app import views

@app.route('/')
def index():
	results = firebase.get('/items', None)
	return render_template('index.html', results=results)

@app.route('/testing')
def testing():
	return "<h1>This is another testing page</h1>"

count = 0

@app.route('/submission', methods=['GET', 'POST'])
def itemSubmission():
	form = submitItem()
	if form.validate_on_submit():
		global count
		count += 1
		putData = {'item' : form.item.data, 'description' : form.description.data, 'name' : form.name.data, 'location' : form.location.data}
		firebase.put('/items', putData['name'] + '/' + putData['item'], putData)
		return render_template('api-put-result.html', form=form, putData=putData)
	return render_template('submit-item.html', form=form)

@app.route('/<name>/<item>')
def viewItem(name, item):
	result = firebase.get('/items', name)
	result = result[item]
	return render_template('fetch-item-result.html', result=result)
