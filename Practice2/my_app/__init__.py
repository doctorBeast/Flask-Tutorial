from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.admin import Admin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/practice2db' #some database uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'some_random_key'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'bprint.login'

import my_app.core.views as views
admin = Admin(app,index_view = views.MyAdminIndexView(
	name = 'HOME',
	url = '/adminhome'))
admin.add_view(views.CompanyView(views.Company,db.session))
admin.add_view(views.AdminView(views.AdminUsers,db.session))

from my_app.core.views import bprint
app.register_blueprint(bprint)

db.create_all()