from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask('schmao')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rocco:dev@localhost/schmao'
db = SQLAlchemy(app)

from schmao.models import *
from schmao.controllers import *