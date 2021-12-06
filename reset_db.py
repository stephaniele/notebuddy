print('Resetting database...')
from server import db
# Reset the database
db.db.drop_all()
# Create the tables
db.db.create_all()
# Create a test entry which works somewhat
if (len(db.getUser()) == 0):
    db.create("Qingru","qzhang1@macalester.edu","Student","Macalester College")
print('Database reset: success!')

print(db.getUser()[0].school)