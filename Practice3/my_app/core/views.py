from flask import Blueprint , g
from flask import render_template , redirect , request , session,flash,url_for,abort
from my_app.core.models import RegisterForm,User,LoginForm,AdminUserCreateForm,AdminUserUpdateForm
from my_app import db,api,app
from flask_restful import Resource,reqparse
from werkzeug.security import generate_password_hash
import json
from functools import wraps
from flask.ext.login import current_user,login_required , login_user,logout_user
from my_app import login_manager
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin import BaseView, expose, AdminIndexView
from wtforms import PasswordField

bprint = Blueprint('bprint',__name__)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))

@bprint.before_request
def get_current_user():
	g.user = current_user

@bprint.route('/')
@bprint.route('/home')
def home():
	print(current_user)
	if current_user.is_authenticated:
		return render_template('home.html',user = current_user)

	# if session.get('username'):
	# 	user = User.query.filter_by(username = session.get('username')).first()
	# 	return render_template('home.html',user = user)
	return render_template('home.html',user = None)

@bprint.route('/register',methods = ['GET','POST'])
def register():
	if session.get('username'):
		flash('You are already logged in!!','info')
		redirect(url_for('bprint.home')) #if the username already in session , redirect to home with different message

	form = RegisterForm(request.form)

	if request.method == 'POST' and form.validate():
		username = request.form.get('username')
		password = request.form.get('password')
		existing_username = User.query.filter_by(username = username).all()
		if existing_username:
			flash('Username already exists','danger')
			return render_template('register.html',form = form)

		user = User(username,password,True)
		db.session.add(user)
		db.session.commit()
		flash('You are now register. Continue to Login','success')
		return redirect(url_for('bprint.login'))

	if form.errors:
		flash(form.errors,'danger')

	return render_template('register.html',form=form)

@bprint.route('/login',methods = ['GET','POST'])
def login():
	if session.get('username'):
		flash('You are already logged in!!','success')
		return redirect(url_for('bprint.home'))

	form = LoginForm(request.form)
	print(request.method)
	print(request.form.get('username'))
	print(request.form.get('password'))
	# print(form.validate())
	if request.method == 'POST' and form.validate():
		username = request.form.get('username')
		password = request.form.get('password')
		existing_user = User.query.filter_by(username = username).first()

		# if not (existing_user and existing_user.check_user_password(password)):
		# 	flash('Invalid Username and Password','warning')
		# 	return render_template('login.html',form = form)

		# session['username'] = username
		login_user(existing_user)
		flash('You have successfully logged in.','success')
		return redirect(url_for('bprint.home'))

	print(form.errors)
	if form.errors:
		flash(form.errors,'danger')

	return render_template('login.html',form = form)

@bprint.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out!!')

	return redirect(url_for('bprint.home'))


# From here I will code for the api requests

parser = reqparse.RequestParser()
parser.add_argument('name',type = str)
parser.add_argument('password',type = str)

class UserApi(Resource):
	def get(self,id=None , page = 1):
		if not id:
			users = User.query.paginate(page,10).items
		else:
			users = [User.query.get(id)]

		print('******')	
		print(users)
		print('******')
		if users == [None]:
			print('Helo')
			abort(404)


		res = {}
		for user in users:
			res[user.id] = {
				'name' : user.username,
				'pwdhash' : user.pwdhash
			}
		return json.dumps(res)

	def post(self):
		args = parser.parse_args()
		name = args['name']
		password = args['password']

		existing_username = User.query.filter_by(username = name).first()
		if existing_username:
			return json.dumps({'Status':'Username Exists'})

		user = User(name,password)
		db.session.add(user)
		db.session.commit()
		res = {}
		res[user.id] = {
			'username' : user.username,
			'pwdhash' : user.pwdhash
		}

		return json.dumps(res)

	def put(self,id):
		args = parser.parse_args()
		name = args['name']
		password = args['password']
		existing_username = User.query.filter_by(username = name).first()

		if existing_username:
			return json.dumps({'Status':'Username already exists'})

		User.query.filter_by(id = id).update({
			'username' : name,
			'pwdhash' : generate_password_hash(password)
			})
		db.session.commit()
		user = User.query.get_or_404(id)

		res = {}
		res[user.id] = {
			'username' : user.username,
			'pwdhash' : user.pwdhash
		}

		return json.dumps(res)


	def delete(self,id):
		user = User.query.filter_by(id = id)
		user.delete()
		db.session.commit()
		return json.dumps({'Status':'User deleted.'})
		
api.add_resource(
	UserApi,
	'/api/user',
	'/api/user/<int:id>',
	'/api/user/<int:id>/<int:page>'
	)

# Below this I will write code for Admin Authentication

def admin_login_required(func):
	@wraps(func)
	def decorated_view(*args,**kwargs):
		print('Inside decorated view.')
		if not current_user.is_admin(): # Where have we defined current_user
			return abort(403)
		return func(*args,**kwargs)
	return decorated_view

# @bprint.route('/admin')
# @login_required #We have not imported login_required
# @admin_login_required
# def home_admin():
# 	return render_template('admin-home.html') #Not created admin-home.html

# @bprint.route('/admin/users-list')
# @login_required #We have not imported login_required
# @admin_login_required
# def users_list_admin():
# 	users = User.query.all()
# 	return render_template('users-list-admin.html',users = users) # Not created the corresponding html file

# @bprint.route('/admin/create-user',methods = ['GET','POST'])
# @login_required
# @admin_login_required
# def user_create_admin():
# 	form = AdminUserCreateForm(request.form) #page no. 140 continue to type code from here.

# 	if form.validate():
# 		username = form.username.data
# 		password = form.password.data
# 		admin = form.admin.data
# 		existing_username = User.query.filter_by(username = username).first()
# 		if existing_username:
# 			flash('This username has already been taken. Try another ','warning')
# 			return render_template('user-create-admin.html',form = form) #Check if the already created register.html is the one that is required here.
			
# 		user = User(username,password,admin)
# 		db.session.add(user)
# 		db.session.commit()
# 		flash('New User Created.','info')
# 		return redirect(url_for('bprint.users_list_admin'))

# 	if form.errors:
# 		flash(form.errors,'danger')

# 	return render_template('user-create-admin.html',form = form) # Not created the corresponding html file.


# @bprint.route('/admin/update-user/<id>',methods = ['GET','POST'])
# @login_required
# @admin_login_required
# def user_update_admin(id = None):
# 	user = User.query.get(id)
# 	form = AdminUserUpdateForm(request.form,
# 		username = user.username,
# 		admin = user.admin
# 		)

# 	if form.validate():
# 		username = form.username.data
# 		admin = form.admin.data

# 		User.query.filter_by(id = id).update({
# 				'username':username,
# 				'admin':admin,
# 			})

# 		db.session.commit()
# 		flash('User Updated.','info')
# 		return redirect(url_for('bprint.users_list_admin'))

# 	if form.errors:
# 		flash(form.errors,'danger')

# 	return render_template('user-update-admin.html',form = form,user = user) # Create the corresponding html file


# @bprint.route('/admin/delete-user/<id>')
# @login_required
# @admin_login_required
# def user_delete_admin(id): # Have to use this method on a POST request.
# 	user = User.query.get(id)
# 	user.delete()

# 	db.session.commit()
# 	flash('User Deleted.')
# 	return redirect(url_for('bprint.users_list_admin'))

# Registering models with Flask Admin.

# class HelloView(BaseView):
# 	@expose('/')
# 	def index(self):
# 		return self.render('hello.html')

# 	def is_accessible(self):
# 		return current_user.is_authenticated() and current_user.is_admin()

class MyAdminIndexView(AdminIndexView):
	def is_accessible(self):
		return current_user.is_authenticated and current_user.is_admin()


class UserAdminView(ModelView):
	column_searchable_list = ('username',)
	column_sortable_list = ('username','admin')
	column_exclude_list = ('pwdhash',)
	form_excluded_columns = ('pwdhash',)
	form_edit_rules = ('username','admin')

	def is_accessible(self):
		return current_user.is_authenticated()


	def scaffold_form(self):
		form_class = super(UserAdminView, self).scaffold_form()
		form_class.password = PasswordField('Password')
		return form_class

	def create_model(self,form):
		model = self.model(
			form.username.data,form.password.data,form.admin.data
			)
		form.populate_obj(model)
		self.session.add(model)
		self._on_model_change(form, model, True)
		self.session.commit()