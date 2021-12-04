from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class UserDatabase:
    def __init__(self, app):
	    db = SQLAlchemy(app)
	    self.db = db
	    self.user_model = userFactory(db)

    def get(self, id=None):
		if id:
			return self.model.query.get(id)
		return self.model.query.all()

	def create(self, id, username, email):
	    user = self.model(id, username, email)
		self.db.session.add(user)
		self.db.session.commit()

	def update(self, id, username, email):
		user = self.get(id)
		user.username = username
		user.email = email
		self.db.session.commit()

	def delete(self, id):
		id = self.get(id)
		self.db.session.delete(review)
		self.db.session.commit()
 
def userFactory(db):
    class UserModel(UserMixin, db.Model):
        __tablename__ = 'users'
 
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(100))
        email = db.Column(db.String(80), unique=True)
        password_hash = db.Column(db.String())
    
        def __init__(self, username, email, password):
		    self.username = username
		    self.email = email
		    self.password = password
 
        def generate_hash(self, password):
            self.password_hash = generate_password_hash(password)
     
        def check_password(self, password):
            return check_password_hash(self.password_hash,password)

        return UserModel

