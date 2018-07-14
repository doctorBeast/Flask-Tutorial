from my_app import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_wtf import Form 
from wtforms import TextField , PasswordField , BooleanField
from wtforms.validators import InputRequired , EqualTo , Length

class User(db.Model):
	id = db.Column(db.Integer , primary_key = True)
	username = db.Column(db.String(10))
	pwdhash = db.Column(db.String())
	admin = db.Column(db.Boolean())

	def __init__(self,username,password,admin = False):
		self.username = username
		self.pwdhash = generate_password_hash(password) #here I need to generate_password_hash of password input
		self.admin = admin

	def check_user_password(self,password):
		return check_password_hash(self.pwdhash,password)

	def is_admin(self):
		return self.admin

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return self.id

class LoginForm(Form):
	username = TextField('Username', [InputRequired()]) #add validators to check if username exists.
	password = PasswordField('Password',[InputRequired()]) #add validators for password not correct.

	# Can't exactly understand the working of the methods below.
	# def __init__(self,*args,**kwargs):
	# 	Form.__init__(self,*args,**kwargs)
	# 	self.user = None

	def validate(self):
		rv = Form.validate(self)
		if not rv:
			return False

		user = User.query.filter_by(username = self.username.data).first()
		if user is None:
			self.username.errors.append('Unknown Username')
			return False

		if not user.check_user_password(self.password.data):
			print('inside login form checking password %s'% self.password.data)
			self.password.errors.append('Invalid Password')
			return False

		# self.user = user
		return True



class RegisterForm(Form):
	username = TextField('Username',[InputRequired(),Length(max = 10)]) # also add validators to check if the username doesnot exist
	password = PasswordField('Password',[InputRequired(),EqualTo('confirm_password',message = 'The passwords must match.')])
	confirm_password = PasswordField('Confirm Password',[InputRequired()])

class AdminUserCreateForm(Form):
	username = TextField('Username',[InputRequired()])
	password = PasswordField('Password',[InputRequired()])
	admin = BooleanField('Is Admin ?')

class AdminUserUpdateForm(Form):
	username = TextField('Username',[InputRequired()])
	admin = BooleanField('Is Admin ?')

