from flask_sqlalchemy import SQLAlchemy


class Database:
    def __init__(self, app):
        db = SQLAlchemy(app)
        self.db = db
        self.User = userFactory(db)
        self.File = fileFactory(db)    
        self.UsersOfWorkspace = usersOfWorkspaceFactory(db)
        self.Workspace = workspaceFactory(db,self.UsersOfWorkspace)


        
    def getUser(self, id=None):
        if id:
            return self.User.query.get(id)
        return self.User.query.all()

    def getFile(self, id=None):
        if id:
            return self.File.query.get(id)
        return self.File.query.all()

    def getWorkspace(self, id=None):
        if id:
            return self.Workspace.query.get(id)
        return self.Workspace.query.all()

    def createUser(self, name,email,occupation,school):
        user = self.User(name,email,occupation,school)
        self.db.session.add(user)
        self.db.session.commit()
    
    def createFile(self, name,email,occupation,school,owner_id):
        file = self.File(name,email,occupation,school,owner_id)
        self.db.session.add(file)
        self.db.session.commit()

    def createWorkspace(self, name,email,occupation,school,owner_id):
        workspace = self.Workspace(name,email,occupation,school,owner_id)
        self.db.session.add(workspace)
        self.db.session.commit()

    def update(self, id, title, text, rating):
        review = self.get(id)
        review.title = title
        review.text = text
        review.rating = rating
        self.db.session.commit()

    def delete(self, id):
        review = self.get(id)
        self.db.session.delete(review)
        self.db.session.commit()

def userFactory(db):
    class User(db.Model):
        __tablename__ = 'user'
        id = db.Column('user_id', db.Integer, primary_key=True)
        name = db.Column(db.String)
        email = db.Column(db.String)
        occupation = db.Column(db.String)
        school = db.Column(db.String)

        # one to many 
        files = db.relationship('File',backref='owner', lazy='select')

        def __init__(self, name, email, occupation, school):
            self.name = name
            self.email = email
            self.occupation = occupation
            self.school = school
    return User

def fileFactory(db):
    class File(db.Model):
        __tablename__ = 'file'
        id = db.Column('file_id', db.Integer, primary_key=True)
        name = db.Column(db.String)
        occupation = db.Column(db.String)
        school = db.Column(db.String)

        # many to one
        owner_id = db.Column(db.Integer, db.ForeignKey('user.user_id'),
        nullable=False)

        def __init__(self, name, email, occupation, school,owner):
            self.name = name
            self.email = email
            self.occupation = occupation
            self.school = school
            self.owner = owner
    return File

def usersOfWorkspaceFactory(db):
    usersOfWorkspace= db.Table('usersOfWorkspace',
        db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'), primary_key=True),
        db.Column('workspace_id', db.Integer, db.ForeignKey('workspace.workspace_id'), primary_key=True)
    )
    return usersOfWorkspace

def workspaceFactory(db,usersOfWorkspace):
    class Workspace(db.Model):
        __tablename__ = 'workspace'
        id = db.Column('workspace_id', db.Integer, primary_key=True)
        name = db.Column(db.String)
        startDate = db.Column(db.DateTime)
        endDate = db.Column(db.DateTime)


        # many to many
        users = db.relationship('user', secondary=usersOfWorkspace, lazy='subquery',
        backref=db.backref('workspaces', lazy=True))

        def __init__(self, name, email, occupation, school,owner):
            self.name = name
            self.email = email
            self.occupation = occupation
            self.school = school
            self.owner = owner
    return Workspace