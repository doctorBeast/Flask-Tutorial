from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask.ext.login import LoginManager
from flask.ext.admin import Admin 


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/practice3db' #some database uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key = 'some_random_key'

api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'bprint.login'

import my_app.core.views as views
admin = Admin(app,index_view = views.MyAdminIndexView(
	name = 'HOME',
	url = '/adminhome'))
# admin.add_view(views.HelloView(name = 'Hello'))
admin.add_view(views.UserAdminView(views.User , db.session))

from my_app.core.views import bprint
app.register_blueprint(bprint)



db.create_all()