# Notebuddy

Notebuddy is a website where students can create and join workspaces, inside which they can upload their notes to share with each other.


### Setting up the environment and running the app

1. Make sure you have python3 and pip3 installed
2. Go to the project directory and start a virtual environment
```
python3 -m venv [name]
source [name]/bin/activate
```
3. Install project dependencies in your virtual environment. This makes sure that all of our dependencies are synced up:

```
pip3 install -r requirements.txt
```
4. Run reset_db.py to create a database:

```
python3 reset_db.py
```
5. Run server.py to start the app:

```
python3 server.py
```

Everything up to date and ready to run!
