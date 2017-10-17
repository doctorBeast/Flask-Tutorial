from flask import Flask,request,render_template


app = Flask(__name__)

@app.route('/profile/<name>')
def profile(name):
	return render_template("profile.html", name= name)

@app.route('/bacon',methods = ['GET','POST'])
def bacon():
	if request.method == 'POST':
		return "You are using post"
	else:
		return "you r using get method"

@app.route('/profi/<user>')
def profi(user):
	return 'hello %s' % user

@app.route('/prof/<int:post_id>')
def profit(post_id):
	return 'hello there %d' % post_id

if __name__ == "__main__":
	app.run(debug = True)

