import os
from flask import Flask, flash, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from database import Database

app = Flask(__name__)
app.config.from_pyfile('server.cfg')

db = Database(app)

@app.route("/") 
def index():
    return render_template("homepage.html")

@app.route("/home")
def home():
    return("This is where your workspaces are")

@app.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        return redirect('/home')
    return render_template("accountform.html", action = "/sign_in", title = "Sign In")

@app.route("/create_account", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        title=request.form["title"]
        review=request.form["review"]
        rating=request.form["rating"]
        db.create(title, review, rating)
        return redirect('/')
    else:
        return render_template("accountform.html", action = "/create_account", title = "Create Account")

@app.route("/workspace")
def workspace():
    return render_template("workspace.html")

# @login_manager.user_loader
# def load_user(user_id):
#     return UserModel.query.get(int(user_id))

if __name__ == '__main__':
    app.run(debug=True)