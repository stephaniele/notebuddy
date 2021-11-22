import os
from flask import Flask, flash, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route("/") 
def index():
    return render_template("homepage.html")

@app.route("/home")
def home():
	return("This is where your workspaces are")

@app.route("/workspace")
def workspace():
	return render_template("workspace.html")

if __name__ == '__main__':
    app.run(debug=True)