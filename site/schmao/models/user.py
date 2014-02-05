from schmao import db

flags = db.Table('flags',
	db.Column('chall_id', db.Integer, db.ForeignKey('challenge.id')),
	db.Column('user_id', db.Integer, db.ForeignKey('user.id')))

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(120))
  flags = db.relationship('Challenge', secondary=flags, 
  	backref=db.backref('solves', lazy='dynamic'))

  def __init__(self, name):
  	self.name = name

  def __repr__(self):
  	return '<User %r>' % self.name