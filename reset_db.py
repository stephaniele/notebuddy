print('Resetting database...')
from server import db, workspace
# Reset the database
db.db.drop_all()
# Create the tables
db.db.create_all()
# Create a test entry which works somewhat
if (len(db.getUser()) == 0):
    db.createUser("Qingru","qzhang1@macalester.edu","Student","Macalester College")
print('Database reset: success!')

user1 = db.getUser()[0]
db.createFile("a","b","c","d",user1)
db.createWorkspace("a","b","c","d",user1)


file1 = db.getFile()[0]
workspace1=db.getWorkspace()[0]

print(user1.id)
print(file1.owner_id)
print(user1.files)
print(user1.workspaces)
print(workspace1.users)