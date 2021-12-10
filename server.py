import os
from flask import Flask, flash, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from database import Database, userFactory
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime, timedelta
import random
import string



app = Flask(__name__)
app.config.from_pyfile('server.cfg')

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


db = Database(app)
login_manager = LoginManager()
login_manager.init_app(app)

@app.route("/")
def go_to_sign_in():
    return redirect("sign_in")

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
        return redirect('/sign_in')
    else:
        return render_template("accountform.html", action = "/create_account", title = "Create Account")

@app.route("/homepage") 
@login_required
def index():
    
    return render_template("homepage.html", workspaces = current_user.workspaces, current_user=current_user)

@app.route("/logout") 
@login_required
def logout():
    logout_user()
    return redirect("/sign_in")

@app.route('/edit_profile',methods=["POST","GET"])
@login_required
def edit_profile():
    if request.method == "POST":
        name = request.form["username"]
        school = request.form["school"]
        occupation = request.form["occupation"]

        if name:
            current_user.updateName(name)
        if school:
            current_user.updateSchool(school)
        if occupation:
            current_user.updateOccupation(occupation)
    return redirect("/homepage")

@app.route('/quit_workspace/<id>',methods=["POST","GET"])
@login_required
def quit_workspace(id):
    workspace = db.Workspace.get(id)
    db.deleteUserFromWorkspace(current_user,workspace)
    return redirect("/homepage")

@app.route('/create_workspace',methods=["POST","GET"])
@login_required
def create_workspace():
    if request.method == "POST":
        name = request.form["workspace_name"]
        description = request.form["workspace_description"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]

        datetime_start_date = datetime.strptime(start_date, '%Y-%m-%d')
        datetime_end_date = datetime.strptime(end_date, '%Y-%m-%d')


        # Transform days of week to a string
        Monday = request.form.get("Monday")
        Tuesday = request.form.get("Tuesday")
        Wednesday = request.form.get("Wednesday")
        Thursday = request.form.get("Thursday")
        Friday = request.form.get("Friday")
        
        days_of_week_str = ""
        if (Monday == "on"):
            days_of_week_str += "1"
        if (Tuesday == "on"):
            days_of_week_str += "2"
        if (Wednesday == "on"):
            days_of_week_str += "3"
        if (Thursday == "on"):
            days_of_week_str += "4"
        if (Friday == "on"):
            days_of_week_str += "5" 
        
        if datetime_start_date > datetime_end_date:
            flash("Sorry, you didn't successfully create a new workspace. It seems that you chose a start date later than the end date.")
            return redirect("/homepage")

        if len(days_of_week_str) == 0:
            flash("Sorry, you didn't successfully create a new workspace. It seems that you didn't select any days of the week.")
            return redirect("/homepage")
        
        letters = string.ascii_lowercase
        secretCode = ''.join(random.choice(letters) for i in range(10)) + name

        workspace = db.Workspace.create(name,description,datetime_start_date,datetime_end_date,days_of_week_str,secretCode)
        
        db.addUserToWorkspace(current_user,workspace)
        return redirect("/homepage")


# @app.route("/uploadfile/<workspace_id>", methods=["POST"])
# def uploadFile(workspace_id):
#     workspace = db.Workspace.get(workspace_id)
#     if request.method == "POST":
#         if 'file' not in request.files:
#             flash('No selected file')
#             return redirect("/workspace/"+workspace_id)
#         rawfile = request.files['file']
#         if rawfile.filename == '':
#             flash('No selected file')
#             return redirect("/workspace/"+workspace_id)
#         if rawfile:
#             filename = secure_filename(rawfile.filename) 

#             # save to uploads foler
#             rawfile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

#             # save reference to database
#             file_type= filename.rsplit('.', 1)[1].lower()
#             file_path = "uploads/"+filename       
#             db.File.create(filename,file_path,file_type,current_user,workspace)

#     return render_template("workspace.html", workspace=workspace,days=daysStr)

@app.route("/workspace/<id>", methods=["GET","POST"])
@login_required
def workspace(id):
    workspace = db.Workspace.get(id)
    daysOfWeek = workspace.dayOfWeek
    startDate = workspace.startDate
    endDate = workspace.endDate
    duration = endDate-startDate
    days = []
    workspace_days = {}
    days_convert = {
        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday",
        7: "Sunday"
    }

    for i in range(0,len(daysOfWeek)):
        days.append(int(daysOfWeek[i]))  
    for i in range(duration.days):
        dayInt = int((startDate + timedelta(days=i)).weekday())
        if dayInt in days:
            # datetime object as key
            day = datetime.strftime(startDate + timedelta(days=i), '%Y-%m-%d')
            workspace_days[day] = {}
            # dictionary as value
            workspace_days[day]["weekday"] = dayInt
            workspace_days[day]["dayStr"] = str(days_convert.get(dayInt)) + ", " + str((startDate + timedelta(days=i)).month)+"/"+ str((startDate + timedelta(days=i)).day)
            workspace_days[day]["files"] = []
            
    if request.method == "GET":
        return render_template("workspace.html", workspace=workspace,days=workspace_days)

    else:
        upload_date = request.form["add-date"]
        if 'file' not in request.files:
            flash('No selected file')
            return redirect("/workspace/"+workspace_id)
        rawfile = request.files['file']
        if rawfile.filename == '':
            flash('No selected file')
            return redirect("/workspace/"+workspace_id)
        if rawfile:
            filename = secure_filename(rawfile.filename) 

            # save to uploads foler
            rawfile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # save reference to database
            file_type= filename.rsplit('.', 1)[1].lower()
            file_path = "uploads/"+filename
            file = db.File.create(filename,file_path,file_type,current_user,workspace,upload_date)

            # add file to workspace
            db.addFileToWorkspace(file,workspace)

            # add file to workspace day
            workspace_days.get(upload_date)["files"].append(file)
            # print(workspace_days)
            print(db.File.get())

        return render_template("workspace.html", workspace=workspace,days=workspace_days)


@login_manager.user_loader
def load_user(user_id):
    return db.User.getById(user_id)

if __name__ == '__main__':
    app.run(debug=True)
    
    