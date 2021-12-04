from flask_sqlalchemy import SQLAlchemy

class Database:
    def __init__(self, app):
        db = SQLAlchemy(app)
        self.db = db
        self.user_model = UserModel(db)
        self.file_model = FileModel(db)
        

def UserModel(db):
    class User(db.Model):
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
        
        def get(self, id=None):
            if id:
                return self.user_model.query.get(id)
            return self.user_model.query.all()
  
        def create(self, id, username, email):
            user = self.user_model(id, username, email)
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
    return User

def FileModel(db):
    class File(db.Model):
        __tablename__ = 'files'
        id = db.Column('file_id', db.Integer, primary_key=True)
        name = db.Column(db.String)
        occupation = db.Column(db.String)
        school = db.Column(db.String)

        # many to one
        owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'),
        nullable=False)

        def __init__(self, name, email, occupation, school):
            self.name = name
            self.email = email
            self.occupation = occupation
            self.school = school
    return File
