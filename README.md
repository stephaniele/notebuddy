# notebuddy

How to start development server

1. Make sure you have python3 and pip3 installed
2. Go to the project directory and start the virtual environment
```
source venv/bin/activate
```
3. Install project dependencies in your virtual environment. This makes sure that all of our dependencies are synced up:

```
pip3 install -r requirements.txt
```

4. If you install other dependencies later, make sure to include them in requirements.txt by typing the command:
```
pip3 freeze > requirements.txt
```
