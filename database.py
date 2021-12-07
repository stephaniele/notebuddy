from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

class Database:
    def __init__(self, app):
        db = SQLAlchemy(app)
        self.db = db
        self.User = userFactory(db)
        self.File = fileFactory(db)    
        self.UsersOfWorkspace = usersOfWorkspaceFactory(db)
        self.Workspace = workspaceFactory(db,self.UsersOfWorkspace)

    def addUserToWorkspace(self,user_id,workspace_id):
        workspace = self.Workspace.get(workspace_id)
        user = self.User.getById(user_id)
        workspace.users.append(user)
        self.db.session.commit()

    def delete(self, id):
        review = self.get(id)
        self.db.session.delete(review)
        self.db.session.commit()

def userFactory(db):
    class User(db.Model, UserMixin):
        __tablename__ = 'user'
        id = db.Column('user_id', db.Integer, primary_key=True)
        name = db.Column(db.String)
        email = db.Column(db.String)
        occupation = db.Column(db.String)
        school = db.Column(db.String)

        # one to many 
        files = db.relationship('File',backref='owner', lazy='select')

        def __init__(self, name, email, occupation, school, password):
            self.name = name
            self.email = email
            self.occupation = occupation
            self.school = school

        def getAll():
            return User.query.all()
    
        def getById(id):
            return User.query.get(id)
    
        def getByEmail(email):
            return User.query.filter_by(email=email).first()

        def create(name,email,occupation,school,password):
            user = User(name,email,occupation,school,password)
            db.session.add(user)
            db.session.commit()

        def updateName(self,name):
            self.name = name
            db.session.commit()

        def updateEmail(self,email):
            self.email = email
            db.session.commit()

        def updateSchool(self, school):
            self.school = school
            db.session.commit()
    return User

def fileFactory(db):
    class File(db.Model):
        __tablename__ = 'file'
        id = db.Column('file_id', db.Integer, primary_key=True)
        name = db.Column(db.String)
        file_path = db.Column(db.String)
        file_type = db.Column(db.String)

        # many to one
        owner_id = db.Column(db.Integer, db.ForeignKey('user.user_id'),
        nullable=False)
        workspace_owner_id = db.Column(db.Integer, db.ForeignKey('workspace.workspace_id'),
        nullable=False)

        # many to one
        workspace_owner_id = db.Column(db.Integer, db.ForeignKey('workspace.workspace_id'), nullable=False)

        def __init__(self, name, file_path,file_type,owner,workspace_owner):
            self.name = name
            self.file_path=file_path
            self.file_type=file_type
            self.owner = owner
            self.workspace_owner = workspace_owner

        def get(id=None):
            if id:
                return File.query.get(id)
            return File.query.all()

        def create(name,file_path,file_type,owner,workspace_owner):
               file = File(name,file_path,file_type,owner,workspace_owner)
               db.session.add(file)
               db.session.commit()

        def updatePath(self,path):
               self.file_path=path
               db.session.commit()

        def updateName(self,name):
            self.name = name
            db.session.commit()
    return File

def usersOfWorkspaceFactory(db):
    usersOfWorkspace= db.Table('usersOfWorkspace', db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'), primary_key=True), db.Column('workspace_id', db.Integer, db.ForeignKey('workspace.workspace_id'), primary_key=True))
    return usersOfWorkspace

def workspaceFactory(db,usersOfWorkspace):
    class Workspace(db.Model):
        __tablename__ = 'workspace'
        id = db.Column('workspace_id', db.Integer, primary_key=True)
        name = db.Column(db.String)
        description = db.Column(db.String)
        startDate = db.Column(db.DateTime)
        endDate = db.Column(db.DateTime)

        # one to many
        files = db.relationship('File',backref='workspace_owner', lazy='select')
        # many to many
        users = db.relationship('User', secondary=usersOfWorkspace, lazy='subquery',
        backref=db.backref('workspaces', lazy=True))

        def __init__(self, name, startDate,endDate):
            self.name = name
            self.startDate = startDate
            self.endDate = endDate
            # self.owner = owner

        def get(id=None):
            if id:
                return Workspace.query.get(id)
            return Workspace.query.all()

        def create(name,startDate,endDate):
            workspace = Workspace(name,startDate,endDate)
            db.session.add(workspace)
            db.session.commit()

        def updateDescription(self,description):
            self.description = description
            db.session.commit()
    return Workspace
