print('Resetting database...')
from server import db, workspace
import datetime

x = datetime.datetime(2020, 5, 17)

# Reset the database
db.db.drop_all()
# Create the tables
db.db.create_all()
# Create a test entry which works somewhat
if (len(db.User.get()) == 0):
    db.User.create("Qingru","qzhang1@macalester.edu","Student","Macalester College")
    db.User.create("Carrie","qzhang1@macalester.edu","Student","Macalester College")

print('Database reset: success!')

# Create user
user1 = db.User.get()[0]
user2 = db.User.get()[1]

# Update user info
user1.updateName("Stephanie")
# print(user1.name)
# print(user1.email)

# Create workspace
db.Workspace.create("a",x,x)
workspace1 = db.Workspace.get()[0]

# Update workspace info
workspace1.updateDescription("Welcome to our workspace")
print(workspace1.description)

# Create file
db.File.create("a","b","c",user1,workspace1)
db.File.create("12","13","14",user1,workspace1)

# Get file
file1 = db.File.get()[0]
file2 = db.File.get()[1]


# Update file info
print(file1.name)
file1.updateName("comp446-note")
print(file1.name)

# Add user to workspace

db.addUserToWorkspace(1,1)
db.addUserToWorkspace(2,1)

print(file1.owner)
print(file2.owner)
print(file1.workspace_owner)
print(file2.workspace_owner)

print(user1.workspaces)
print(workspace1.users)
