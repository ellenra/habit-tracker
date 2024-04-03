from app import app
from db import db
from flask import render_template, request, redirect, session
from datetime import datetime, timedelta
import users
from habits import addhabits, getdata, update_habit_boolean_value, update_habit_number_value, add_habits_for_the_day, get_form_status

@app.route("/")
def index():
    if not session:
        return render_template("index.html")
    else:
        return redirect("/day")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        if not users.register(username, email, password):
            return render_template("register.html", notification=True, message="Registration failed!")
        return redirect("/habits")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if not users.login(username, password):
        return render_template("index.html", notification=True, message="Log in failed!")
    return redirect("/day")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/day", methods=["GET", "POST"])
def day():
    user_id = session.get('user_id')
    change_day = int(request.args.get('days', 0))
    date = (datetime.now() + timedelta(days=change_day)).strftime("%A, %d.%m.%Y")
    date_for_database = (datetime.now() + timedelta(days=change_day)).strftime("%Y-%m-%d")
    add_habits_for_the_day(user_id, date_for_database)
    habits = getdata(user_id, date_for_database)
    form_status = get_form_status(date_for_database)

    if request.method == "GET":
        return render_template("day.html", date=date, habits=habits, days=change_day, form_status=form_status)

@app.route("/habits", methods=["GET", "POST"])
def habits():
    if request.method == "GET":
        return render_template("habits.html")
    if request.method == "POST":
        user_id = session.get('user_id')
        sleep = request.form.get('sleep')
        workout = request.form.get('workout')
        steps = request.form.get('steps')
        study = request.form.get('study')
        journal = request.form.get('journal')
        meditate = request.form.get('meditate')
        mood = request.form.get('mood')
        addhabits(sleep, workout, steps, study, journal, meditate, mood, user_id)
        return redirect("/")
    
@app.route("/habit_status", methods=["GET", "POST"])
def habit_status():
    if request.method == "POST":
        user_id = session.get('user_id')
        date = request.form.get("date")
        date_object = datetime.strptime(date, "%A, %d.%m.%Y")
        date_for_database = date_object.strftime("%Y%m%d")
        habits = getdata(user_id, date_for_database)
        for habit in habits:
            habit_id = habit.id
            track_number_value = request.form.get("track_value_" + str(habit_id))
            print("TRACKNUMEBR:", track_number_value)
            if track_number_value.lower() == 'true':
                value = request.form.get('number_' + str(habit_id))
                print("VALUETRUE", value)
                update_habit_number_value(habit_id, value)
            else: 
                value = request.form.get('checkbox_' + str(habit_id))
                print("VALUEFALSE", value)
                if value:
                    update_habit_boolean_value(habit_id)
        return redirect("/day")
