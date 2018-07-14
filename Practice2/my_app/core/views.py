from flask import g, Blueprint, render_template, redirect, flash, url_for, abort, request
from my_app import app,login_manager,db
from my_app.core.models import Company, AdminUsers, LoginForm, RegisterForm, AdminLoginForm
from flask.ext.login import current_user, login_required, login_user, logout_user
from flask.ext.admin import AdminIndexView
from flask.ext.admin.form import rules
from flask.ext.admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash
from wtforms import PasswordField

bprint = Blueprint('bprint',__name__)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html') # Create following HTML file.

@login_manager.user_loader
def load_user(id):
	return Company.query.get(int(id))

@bprint.before_request
def get_current_user():
	g.user = current_user

@bprint.route('/')
@bprint.route('/index')
def index():
	return render_template('index.html') # create following HTML file.

@bprint.route('/register',methods = ['GET','POST'])
def register():
	if current_user.is_authenticated:
		flash('You are already logged in','success')
		return redirect(url_for('bprint.home',id = current_user.id))

	form = RegisterForm(request.form)

	if form.validate_on_submit():
		username = request.form.get('username')
		password = request.form.get('password')
		gstin = request.form.get('gstin')
		company_name = request.form.get('company_name')
		email_id = request.form.get('email_id')
		mobile_no = request.form.get('mobile_no')
		address = request.form.get('address')
		deals_in = request.form.get('deals_in')

		company = Company(gstin,company_name,username,password,email_id,mobile_no,address,deals_in)
		db.session.add(company)
		db.session.commit()
		flash('Your company has been created')
		return redirect(url_for('bprint.login'))

	if form.errors:
		flash(form.errors,'danger')

	return render_template('register.html',form = form) # create following HTML file.

@bprint.route('/login',methods = ['GET','POST'])
def login():
	print(current_user.username)
	if current_user.is_authenticated:

		flash('Your are already logged in','success')
		return redirect(url_for('bprint.home',id = current_user.id))

	form = LoginForm(request.form)

	if form.validate_on_submit():
		username = request.form.get('username')

		user = Company.query.filter_by(username = username).first()
		login_user(user)
		flash('You have been loggen in successfully','success')
		return redirect(url_for('bprint.home',id = user.id))

	if form.errors:
		flash(form.errors,'danger')

	return render_template('login.html',form = form) # create the following HTML file.

@bprint.route('/logout',methods = ['GET'])
@login_required
def logout():
	logout_user()
	# print(current_user.username)
	flash('You have been logged out!!')
	return redirect(url_for('bprint.index'))


@bprint.route('/home/<int:id>',methods = ['GET','POST']) #may be this can be done without writing 'int'
@login_required
def home(id):
	company = Company.query.filter_by(id = id).first()
	return render_template('home.html',company = company) # create the following HTML file.

# Get started with designing the admin view.

def admin_login_required(func): # This decorator was never used .
	@wraps(func)
	def decorated_view():
		if not current_user.is_admin:
			flash('Admin User is not logged in!')
			return redirect(url_for('bprint.adminindex'))
		return func(*args,**kwargs)

	return decorated_view

@bprint.route('/adminindex')
def adminindex():
	print(current_user.username)
	if current_user.is_admin:
		flash('You are already logged in!!','success')
		return redirect(url_for('bprint.adminhome'))

	return render_template('adminindex.html') # create the following HTML file.

@bprint.route('/adminlogin',methods=['GET','POST'])
def adminlogin():
	if current_user.is_authenticated and current_user.is_admin():
		flash('You are logged in as admin','success')
		return redirect(url_for('bprint.adminhome'))

	form = AdminLoginForm(request.form)

	if form.validate_on_submit():
		username = request.form.get('username')

		admin = AdminUsers.query.filter_by(username = username).first()
		login_user(admin)
		print('inside adminlogin form validate')
		print(current_user.username)
		return redirect('/adminhome')

	if form.errors:
		flash(form.errors,'danger')	

	return render_template('adminlogin.html',form = form) # create the following HTML file.


class MyAdminIndexView(AdminIndexView):
	def is_accessible(self):

		print('inside MyAdminIndexView')
		print(current_user.is_authenticated() and current_user.is_admin())
		print(current_user.is_authenticated())
		print(current_user.is_admin())
		# print(current_user.permission)
		print(current_user.username)
		return current_user.is_authenticated() and current_user.is_admin()

class CompanyView(ModelView):
	column_searchable_list = ('username',)
	column_sortable_list = ('company_name','username')
	column_exclude_list = ('pwdhash',)
	form_excluded_columns = ('pwdhash',)
	form_edit_rules = ('username')

	def is_accessible(self):
		return current_user.is_admin()

	def scaffold_form(self):
		form_class = super(CompanyView,self).scaffold_form()
		form_class.password = PasswordField('Password')
		return form_class

	def create_model(self,form):
		model = self.model(
			form.username.data,
			form.password.data,
			form.gstin.data,
			form.company_name.data,
			form.mobile_no.data,
			form.email_id.data,
			form.address.data,
			form.deals_in.data
			)
		form.populate_obj(model)
		self.session.add(model)
		self._on_model_change(form,model,True)
		self.session.commit()

class AdminView(ModelView):
	column_searchable_list = ('username','permission')
	column_sortable_list = ('username',)
	column_exclude_list = ('pwdhash')
	form_excluded_columns = ('pwdhash')
	form_edit_rules = ('username','permission',rules.Header('Reset Password'),'new_password','confirm')
	form_create_rules = ('username','permission','password')

	def is_accessible(self):
		return current_user.is_admin()

	def scaffold_form(self):
		form_class = super(AdminView,self).scaffold_form()
		form_class.password = PasswordField('Password')
		form_class.new_password = PasswordField('New Password')
		form_class.confirm = PasswordField('Confirm New Password')

		return form_class

	def create_model(self,form):
		model = self.model(
			form.username.data,form.password.data,form.permission.data)
		form.populate_obj(model)
		self.session.add(model)
		self._on_model_change(form,model,True)
		self.session.commit()

	def update_model(self,form,model):
		form.populate_obj(model)
		if form.new_password.data :
			if form.new_password.data != form.confirm.data:
				flash('Passwords must match')
				return
			model.pwdhash = generate_password_hash(form.new_password.data)
		self.session.add(model)
		self._on_model_change(form,model,False)
		self.session.commit()