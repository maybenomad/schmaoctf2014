from flask import Flask
import os
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask('schmao')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rocco:dev@localhost/schmao'
db = SQLAlchemy(app)
app.secret_key = "('S\x86O\xa11\xfcF}_=\x9f@\xec\x171^c5\xb2\x04+\x9d\xe5\xd1\x19\x8c\xaf\xee\x00\x1d"

from schmao.models import *
from schmao.controllers import *