class Challenge(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(120))
  desc = db.Column(db.Text)
  points = db.Column(db.Integer)
  category = db.Column(db.String(80))
  flag = db.Column(db.String(64))

  def __init__(self, name, desc, points, flag):
    self.name = name
    self.desc = desc
    self.points = points
    self.category = category
    self.flag = flag
    
  def __repr__(self):
    return '<Challenge %r>' % self.name
