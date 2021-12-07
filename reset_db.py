print('Resetting database...')
from server import db, workspace
import datetime

x = datetime.datetime(2020, 5, 17)

# Reset the database
db.db.drop_all()
# Create the tables
db.db.create_all()
# Create a test entry which works somewhat
if (len(db.getUser()) == 0):
    db.createUser("Qingru","qzhang1@macalester.edu","Student","Macalester College")
    db.createUser("Carrie","qzhang1@macalester.edu","Student","Macalester College")

print('Database reset: success!')

user1 = db.getUser()[0]
user2 = db.getUser()[1]

db.createWorkspace("a",x,x)
workspace1 = db.getWorkspace()[0]

db.createFile("a","b","c",user1,workspace1)
db.createFile("12","13","14",user1,workspace1)

file1 = db.getFile()[0]
file2 = db.getFile()[1]

db.addUserToWorkspace(1,1)
db.addUserToWorkspace(2,1)

print(file1.owner)
print(file2.owner)
print(file1.workspace_owner)
print(file2.workspace_owner)

print(user1.workspaces)
print(workspace1.users)
