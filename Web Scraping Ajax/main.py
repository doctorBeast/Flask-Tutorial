from flask import Flask 
from flask import render_template,request
from process_data import *

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/search',methods = ['POST'])
def search():
	print('hello')
	station_name = request.form.get('station_name')
	start_time = request.form.get('start_time')
	end_time = request.form.get('end_time')
	text = func(station_name , start_time , end_time)
	print(type(text))
	return render_template('search.html', html = text)

if __name__ == '__main__':
	app.run(debug = True)