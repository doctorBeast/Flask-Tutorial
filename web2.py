from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/web2db'
db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer,primary_key = True)
	username = db.Column(db.String(80),unique = True)
	email = db.Column(db.String(120),unique = True)
	about = db.Column(db.String(120))

	def __init__(self,username,email):
		self.username = username
		self.email = email

	def __repr__(self):
		return '<User %r>' % self.username	

@app.route('/')
def index():
	myUser = User.query.all()
	onetime = User.query.filter_by(email= 'jkl' ).all()
	print(myUser[0].about)
	return render_template('barry.html', myUser = myUser,onetime = onetime)

@app.route('/profile',methods = ['POST'])
def profile():

	name = request.form['querry']
	twotime = User.query.filter_by(username = name).first()
	return "<label>Here is the About of that User: %s</label>" %twotime.about
				

@app.route('/post_user',methods = ['POST'])
def post_user():
	user = User(request.form['username'],request.form['email'])
	db.session.add(user)
	db.session.commit()
	return redirect(url_for('index'))

if __name__ == "__main__":
	app.run(debug = True)

