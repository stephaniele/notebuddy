import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from userdatabase import UserDatabase

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userss.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisissecret'
login_manager = LoginManager()
login_manager.init_app(app)

# databases
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

@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))

if __name__ == '__main__':
    app.run(debug=True)