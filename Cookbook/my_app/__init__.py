from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/testdb'
db = SQLAlchemy(app)
migrate = Migrate(app,db)

manager = Manager(app)
manager.add_command('db',MigrateCommand)


import my_app.catalog.views


db.create_all()
