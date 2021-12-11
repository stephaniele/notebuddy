import os
from flask import Flask, flash, render_template, request, redirect, url_for, jsonify, send_file
from werkzeug.utils import secure_filename
from database import Database, userFactory
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime, timedelta, date
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
    error = None
    if request.method == "POST":
        email=request.form["email"]
        user = db.User.getByEmail(email)
        if user is not None and user.check_password(request.form['password']):
            login_user(user)
            return redirect('/homepage')
        elif user is None:
            error = "Email address wasn't registered"
        elif not user.check_password(request.form['password']):
            error = "Password entered is not correct"
        else:
            error = "Other issue occured"
    return render_template("accountform.html", action = "/sign_in", title = "Sign In", error = error)

@app.route("/create_account", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        username=request.form["username"]
        email=request.form["email"]
        school=request.form["school"]
        occupation=request.form["occupation"]
        password=request.form["password"]
        db.User.create(username, email, occupation, school, password)   
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
        user_data = request.get_json()
        name = user_data[0]["username"]
        occupation = user_data[1]["occupation"]
        school = user_data[2]["school"]
        
        if len(name)>0:
            current_user.updateName(name)
        if len(school)>0:
            current_user.updateSchool(school)
        if len(occupation)>0:
            current_user.updateOccupation(occupation)
    
    results = {'name':name , 'school':school, 'occupation':occupation}

    return jsonify(results)

@app.route('/quit_workspace/<id>',methods=["POST","GET"])
@login_required
def quit_workspace(id):
    workspace = db.Workspace.get(id)
    db.deleteUserFromWorkspace(current_user,workspace)
    return redirect("/homepage")

@app.route('/join_workspace',methods=["POST","GET"])
@login_required
def join_workspace():
    secretCode = request.form["secretCode"]
    workspace = db.Workspace.getBySecretCode(secretCode)[0]
    print(workspace)
    db.addUserToWorkspace(current_user,workspace)
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
            days_of_week_str += "0"
        if (Tuesday == "on"):
            days_of_week_str += "1"
        if (Wednesday == "on"):
            days_of_week_str += "2"
        if (Thursday == "on"):
            days_of_week_str += "3"
        if (Friday == "on"):
            days_of_week_str += "4" 
        
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

@app.route("/upload_file/<id>", methods=["GET","POST"])
@login_required
def upload_file(id):
    workspace = db.Workspace.get(id)
    daysOfWeek = workspace.dayOfWeek
    startDate = workspace.startDate
    endDate = workspace.endDate
    duration = endDate-startDate
    days = []
    workspace_days = {}
    days_convert = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday"
    }
    today = date.today()

    for i in range(0,len(daysOfWeek)):
        days.append(int(daysOfWeek[i]))  
    for i in range(duration.days):
        day = endDate - timedelta(days=i)
        curr_date = day.date()
        dayInt = int(day.weekday())
        if ((dayInt in days) & (curr_date < today)):
            # datetime object as key
            day_key = datetime.strftime(day, '%Y-%m-%d')
            workspace_days[day_key] = {}
            # dictionary as value
            workspace_days[day_key]["id"] = str(days_convert.get(dayInt)+str(day.year)+str(day.month)+ str(day.day))
            workspace_days[day_key]["dayStr"] = str(days_convert.get(dayInt)) + ", " + str(day.month)+"/"+ str(day.day)
            workspace_days[day_key]["files"] = []
    
    upload_date = request.form["add-date"]
    upload_date_datetime = datetime.strptime(upload_date, '%Y-%m-%d')

    if upload_date_datetime.weekday() not in days:
        flash('Please pick a valid day in the workspace')
        return redirect("/workspace/"+id)

    if 'file' not in request.files:
        flash('No selected file')
        return redirect("/workspace/"+id)
    rawfile = request.files['file']
    if rawfile.filename == '':
        flash('No selected file')
        return redirect("/workspace/"+id)
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

        return redirect("/workspace/"+id)



@app.route("/workspace/<id>")
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
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday"
    }
    today = date.today()

    for i in range(0,len(daysOfWeek)):
        days.append(int(daysOfWeek[i]))  
    for i in range(duration.days):
        day = endDate - timedelta(days=i)
        curr_date = day.date()
        dayInt = int(day.weekday())
        if ((dayInt in days) & (curr_date< today)):
            # datetime object as key
            day_key = datetime.strftime(day, '%Y-%m-%d')
            workspace_days[day_key] = {}
            # dictionary as value
            workspace_days[day_key]["id"] = str(days_convert.get(dayInt)+str(day.year)+str(day.month)+ str(day.day))
            workspace_days[day_key]["dayStr"] = str(days_convert.get(dayInt)) + ", " + str(day.month)+"/"+ str(day.day)
            print(str(days_convert.get(dayInt)))
            workspace_days[day_key]["files"] = []
    
    
    workspace_files = workspace.files
    for file in workspace_files:
        upload_date = file.upload_date
        workspace_days.get(upload_date)["files"].append(file)

    return render_template("workspace.html", workspace=workspace,days=workspace_days,today=today)


@app.route('/workspace/download_note/<file_id>')
@login_required
def download_note(file_id):
    file_path = db.File.get(file_id).file_path
    return send_file(file_path, as_attachment=True)
    
@login_manager.user_loader
def load_user(user_id):
    return db.User.getById(user_id)

if __name__ == '__main__':
    app.run(debug=True)
    
    