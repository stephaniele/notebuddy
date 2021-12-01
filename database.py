# class Database:
# 	def __init__(self, app):
# 		db = SQLAlchemy(app)
# 		self.db = db
# 		self.User = UserModel(db)
# 		self.File = FileModel(db)

# 	# def get(self, id=None):
# 	# 	if id:
# 	# 		return self.model.query.get(id)
# 	# 	return self.model.query.all()

# 	# def create(self, title, text, rating):
# 	# 	review = self.model(title, text, rating)
# 	# 	self.db.session.add(review)
# 	# 	self.db.session.commit()

# 	# def update(self, id, title, text, rating):
# 	# 	review = self.get(id)
# 	# 	review.title = title
# 	# 	review.text = text
# 	# 	review.rating = rating
# 	# 	self.db.session.commit()

# 	# def delete(self, id):
# 	# 	review = self.get(id)
# 	# 	self.db.session.delete(review)
# 	# 	self.db.session.commit()

# def UserModel(db):
# 	class User(db.Model):
# 		__tablename__ = 'users'
# 		id = db.Column('user_id', db.Integer, primary_key=True)
# 		name = db.Column(db.String)
# 		email = db.Column(db.String)
# 		occupation = db.Column(db.String)
# 		school = db.Column(db.String)

# 		# one to many 
# 		files = db.relationship('File',backref='owner', lazy='select')

# 		def __init__(self, name, email, occupation, school):
# 			self.name = name
# 			self.email = email
# 			self.occupation = occupation
# 			self.school = school
# 	return User

# def FileModel(db):
# 	class File(db.Model):
# 		__tablename__ = 'files'
# 		id = db.Column('file_id', db.Integer, primary_key=True)
# 		name = db.Column(db.String)
# 		occupation = db.Column(db.String)
# 		school = db.Column(db.String)

# 		# many to one
# 		owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'),
#         nullable=False)

# 		def __init__(self, name, email, occupation, school):
# 			self.name = name
# 			self.email = email
# 			self.occupation = occupation
# 			self.school = school
# 	return File
