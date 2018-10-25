from flask import Flask, render_template, url_for, request, redirect, flash, session, g, abort
from flask_sqlalchemy import SQLAlchemy

# константи(config)
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


app = Flask(__name__)
# знаходить усі змінні у верхньому регістрі
app.config.from_object(__name__)
# загрузка визначень моїх констант з файлу конфігурації
#app.config.from_envvar('FLASKR_SETTINGS', silent = True)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schema.sqlite3'

app.secret_key = SECRET_KEY

db = SQLAlchemy(app)

class Entries(db.Model):
	id = db.Column('entries_id', db.Integer, primary_key=True)
	name = db.Column('name', db.String(20))
	title = db.Column('title', db.String(50))
	text = db.Column('text', db.String(300))
	complete = db.Column('complete', db.Boolean)
	
	def __init__(self, name, title, text, complete):
		self.name = name
		self.title = title
		self.text = text
		self.complete = complete


# функції

@app.route('/')
def show_entries():
	incomplete = Entries.query.filter_by(complete=False).all()
	return(render_template('show_entries.html', incomplete = incomplete, entry_r = None))


@app.route('/add', methods = ['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	else:
		redact = Entries.query.filter_by(title = request.form['title']).first()
		if redact:
			redact.name = request.form['name']
			redact.title = request.form['title']
			redact.text = request.form['text']
			db.session.commit()
			flash('changes was successfully applied')
		else:
			entry = Entries(request.form['name'], request.form['title'], request.form['text'], False)
			db.session.add(entry)
			db.session.commit()
			flash('Record was successfully added')

	return redirect(url_for('show_entries'))


@app.route('/delete/<id>')
def del_entry(id):
	if not session.get('logged_in'):
		abort(401)
	else:
		entry = Entries.query.filter_by(id = int(id)).first()
		entry.complete = True
		db.session.commit()
		return redirect(url_for('show_entries'))

def delete():
	notes = Entries.query.all()
	for note in notes:
		if note.complete == True:
			db.session.delete(note)
	print(' * DB was cleared')


@app.route('/redact/<id>', methods = ['POST', 'GET'])
def redact(id):
	if not session.get('logged_in'):
		abort(401)
	else:
		entry_r = Entries.query.filter_by(id = int(id)).first()
		return (render_template('show_entries.html', entry_r = entry_r))




@app.route('/login', methods = ['POST', 'GET'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config["USERNAME"]:
		   error = "Bad username"

		elif request.form['password'] != app.config["PASSWORD"]:
			 error = 'Bad password'

		else:
			session["logged_in"] = True
			flash('u were logged in')
			return redirect(url_for('show_entries'))

	return render_template("login.html", error = error)


@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash("logout succeded")
	return redirect(url_for('show_entries'))


# очищення бази даних
delete()

if __name__ == "__main__":
	db.create_all()
	app.run(debug = DEBUG)
