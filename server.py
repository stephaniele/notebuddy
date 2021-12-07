import os
from flask import Flask, flash, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from database import Database, userFactory
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config.from_pyfile('server.cfg')

db = Database(app)
login_manager = LoginManager()
login_manager.init_app(app)

@app.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        email=request.form["email"]
        user = db.User.getByEmail(email)
        login_user(user)
        return redirect('/homepage')
    return render_template("accountform.html", action = "/sign_in", title = "Sign In")

@app.route("/create_account", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        username=request.form["username"]
        email=request.form["email"]
        school=request.form["school"]
        occupation=request.form["occupation"]
        password=request.form["password"]
        db.User.create(username, email, password, school, occupation)
        return redirect('/homepage')
    else:
        return render_template("accountform.html", action = "/create_account", title = "Create Account")

@app.route("/homepage") 
# @login_required
def index():
    return render_template("homepage.html")

@app.route("/workspace")
@login_required
def workspace():
    return render_template("workspace.html")

@login_manager.user_loader
def load_user(user_id):
    return db.User.getById(user_id)

if __name__ == '__main__':
    app.run(debug=True)
    
    