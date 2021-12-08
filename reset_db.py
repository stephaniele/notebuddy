print('Resetting database...')
from server import db, workspace
import datetime

x = datetime.datetime(2020, 5, 17)

# Reset the database
db.db.drop_all()
# Create the tables
db.db.create_all()
# Create a test entry which works somewhat
# if (len(db.User.getAll()) == 0):
#     db.User.create("Qingru","qzhang1@macalester.edu","Student","Macalester College","000")
#     db.User.create("Carrie","qzhang1@macalester.edu","Student","Macalester College","000")

# print('Database reset: success!')

# # Create user
# user1 = db.User.getAll()[0]
# user2 = db.User.getAll()[1]

# # Update user info
# user1.updateName("Stephanie")
# # print(user1.name)
# # print(user1.email)

# # Create workspace
# db.Workspace.create("comp446","i love it",x,x,"123")
# workspace1 = db.Workspace.get(1)

# # Update workspace info
# workspace1.updateDescription("Welcome to our workspace")
# print(workspace1.description)

# # Create file
# db.File.create("a","b","c",user1,workspace1)
# db.File.create("12","13","14",user1,workspace1)

# # Get file
# file1 = db.File.get(1)
# file2 = db.File.get(2)


# # Update file info
# print(file1.name)
# file1.updateName("comp446-note")
# print(file1.name)

# # Add user to workspace

# db.addUserToWorkspace(user1,workspace1)


# print(file1.owner)
# print(file2.owner)
# print(file1.workspace_owner)
# print(file2.workspace_owner)

# print(user1.workspaces)
# print(workspace1.users)
