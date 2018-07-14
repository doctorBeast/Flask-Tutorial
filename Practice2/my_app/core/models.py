from my_app import db
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import InputRequired, EqualTo
from flask import flash

class Company(db.Model):
	id = db.Column(db.Integer,primary_key = True)
	join_time = db.Column(db.DateTime, default=datetime.datetime.now)
	gstin = db.Column(db.String(15))
	company_name = db.Column(db.String())
	username = db.Column(db.String())
	pwdhash = db.Column(db.String())
	email_id = db.Column(db.String())
	mobile_no = db.Column(db.String(10)) #Further we can change the string length to 13 (+91,etc) for different countries
	address = db.Column(db.String())
	rating = db.Column(db.Float())
	deals_in = db.Column(db.String())
	no_of_reviews = db.Column(db.Integer)

	def __init__(self, gstin, company_name, username, password, email_id, mobile_no, address, deals_in):
		self.gstin = gstin
		self.company_name = company_name
		self.username = username
		self.pwdhash = generate_password_hash(password)
		self.email_id = email_id
		self.mobile_no = mobile_no
		self.address = address
		self.rating = None
		self.deals_in = deals_in
		self.no_of_reviews = 0

	def __repr__(self):
		return '<%s>' % self.company_name

	def check_user_password(self,password):
		return check_password_hash(self.pwdhash,password)

	def is_authenticated(self):
		return True

	def is_admin(self):
		return False

	def is_anonymous(self):
		return False

	def is_active(self):
		return True

	def get_id(self):
		return self.id


class AdminUsers(db.Model):
	id = db.Column(db.Integer,primary_key = True)
	username = db.Column(db.String())
	pwdhash = db.Column(db.String())
	permission = db.Column(db.String())


	def __init__(self,username,password,permission = 'R'):
		self.username = username
		self.pwdhash = generate_password_hash(password)
		self.permission = permission

	def __repr__(self):
		return '<%s>' % self.username

	def check_user_password(self,password):
		return check_password_hash(self.pwdhash,password)

	def is_admin(self):
		return True

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return self.id




class LoginForm(Form):
	username = TextField('Username',[InputRequired()])
	password = PasswordField('Password',[InputRequired()])

	def validate(self):
		rv = Form.validate(self)
		if not rv:
			return False

		company = Company.query.filter_by(username = self.username.data).first()
		if not company and not company.check_user_password(self.password.data):
			flash('Invalid Username or Password','warning')
			return False

		return True

class RegisterForm(Form):
	username = TextField('Username',[InputRequired()])
	password = PasswordField('Password',[InputRequired()])
	confirm_password = PasswordField('Confirm Password',[InputRequired(),EqualTo('password',message='The passwords must match.')])
	gstin = TextField('GSTIN',[InputRequired()])
	company_name = TextField('Company Name',[InputRequired()])
	email_id = TextField('Email ID',[InputRequired()])
	mobile_no = TextField('Mobile No.',[InputRequired()])
	address = TextField('Address',[InputRequired()])
	deals_in = TextField('Industry Type',[InputRequired()])

	def validate(self):
		rv = Form.validate(self)
		if not rv:
			return False

		# Check for username, confirm email_id, confirm gstin and company, confirm mobile_no, maybe address
		# for now i am only taking care of username

		existing_username = Company.query.filter_by(username = self.username.data).first()
		if existing_username:
			self.username.errors.append('Username Exists')
			return False

		return True

class AdminLoginForm(Form):
	username = TextField('Username',[InputRequired()])
	password = PasswordField('Password',[InputRequired()])

	def validate(self):
		rv = Form.validate(self)
		if not rv:
			return False

		admin = AdminUsers.query.filter_by(username = self.username.data).first()
		if not admin and not admin.check_user_password(self.password.data):
			flash('Invalid username or password','warning')
			return False

		return True




