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
    
    def createFile(self, name,file_path,file_type,owner,workspace_owner):
        file = self.File(name,file_path,file_type,owner,workspace_owner)
        self.db.session.add(file)
        self.db.session.commit()

    def createWorkspace(self, name,startDate,endDate):
        workspace = self.Workspace(name,startDate,endDate)
        self.db.session.add(workspace)
        self.db.session.commit()

    def addUserToWorkspace(self,user_id,workspace_id):
        workspace = self.getWorkspace(workspace_id)
        user = self.getUser(user_id)
        workspace.users.append(user)
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
        file_path = db.Column(db.String)
        file_type = db.Column(db.String)

        # many to one
        owner_id = db.Column(db.Integer, db.ForeignKey('user.user_id'),
        nullable=False)
        workspace_owner_id = db.Column(db.Integer, db.ForeignKey('workspace.workspace_id'),
        nullable=False)

        def __init__(self, name,file_path,file_type,owner,workspace_owner):
            self.name = name
            self.file_path=file_path
            self.file_type=file_type
            self.owner = owner
            self.workspace_owner = workspace_owner
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

        # one to many
        files = db.relationship('File',backref='workspace_owner', lazy='select')

        # many to many
        users = db.relationship('User', secondary=usersOfWorkspace, lazy='subquery',
        backref=db.backref('workspaces', lazy=True))

        def __init__(self, name,startDate,endDate):
            self.name = name
            self.startDate = startDate
            self.endDate = endDate
            # self.owner = owner
    return Workspace