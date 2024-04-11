from app import app
from db import db
from flask import render_template, request, redirect, session
from datetime import datetime, timedelta
import calendar
import users
import habits

@app.route("/")
def index():
    if not session:
        return render_template("index.html")
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
    if request.method == "GET":
        user_id = session.get('user_id')
        change_day = int(request.args.get('days', 0))
        date = (datetime.now() + timedelta(days=change_day)).strftime("%A, %d.%m.%Y")
        date_for_database = (datetime.now() + timedelta(days=change_day)).strftime("%Y-%m-%d")
        habits.add_habits_for_the_day(user_id, date_for_database)
        user_habits = habits.getdata(user_id, date_for_database)
        form_status = habits.get_form_status(date_for_database)
        return render_template("day.html", date=date, habits=user_habits, days=change_day, form_status=form_status)

@app.route("/habits", methods=["GET", "POST"])
def manage_habits():
    if request.method == "GET":
        user_id = session.get('user_id')
        user_habits = habits.gethabits(user_id)
        return render_template("habits.html", habits=user_habits)
    if request.method == "POST":
        user_id = session.get('user_id')
        date_now = datetime.now().strftime("%Y-%m-%d")
        habits.delete_habits(user_id)
        habits.delete_data(user_id, date_now)
        sleep = request.form.get('sleep')
        workout = request.form.get('workout')
        steps = request.form.get('steps')
        study = request.form.get('study')
        journal = request.form.get('journal')
        meditate = request.form.get('meditate')
        mood = request.form.get('mood')
        habits.addhabits(sleep, workout, steps, study, journal, meditate, mood, user_id)
        return redirect("/")
    
@app.route("/habit_status", methods=["GET", "POST"])
def habit_status():
    if request.method == "POST":
        user_id = session.get('user_id')
        date = request.form.get("date")
        date_object = datetime.strptime(date, "%A, %d.%m.%Y")
        date_for_database = date_object.strftime("%Y%m%d")
        user_habits = habits.getdata(user_id, date_for_database)
        edit_status = request.form.get("edit_habits")
        info = None
        for habit in user_habits:
            habit_id = habit.id
            track_number_value = request.form.get("track_value_" + str(habit_id))
            if track_number_value.lower() == 'true':
                value = request.form.get('number_' + str(habit_id))
                habits.update_habit_number_value(habit_id, value)
            else: 
                value = request.form.get('checkbox_' + str(habit_id))
                if value or edit_status:
                    info = True
                    habits.update_habit_boolean_value(habit_id, info)
                else:
                    info = False
                    habits.update_habit_boolean_value(habit_id, info)
        current_day_for_day_route = int(request.form.get("day", 0))
        return redirect(f"/day?days={current_day_for_day_route}")

@app.route("/edit_habits", methods=["GET"])
def edit_habits():
    user_id = session.get('user_id')
    date = request.args.get('date')
    date_object = datetime.strptime(date, "%A, %d.%m.%Y")
    date_for_database = date_object.strftime("%Y%m%d")
    user_habits = habits.getdata(user_id, date_for_database)
    current_day_for_day_route = int(request.args.get('days', 0))
    return render_template("edit_habits.html", habits=user_habits, date=date, days=current_day_for_day_route)

@app.route("/month", methods=["GET"])
def month():
    if request.method == "GET":
        user_id = session.get('user_id')
        get_date = request.args.get('date')
        date = datetime.strptime(get_date, "%A, %d.%m.%Y")
        month_date = date.strftime("%B, %Y")
        date_for_database = date.strftime("%Y%m%d")
        _, days_in_month = calendar.monthrange(date.year, date.month)
        first_day = date.replace(day=1)
        last_day = first_day + timedelta(days=days_in_month - 1)
        current_day = first_day
        habits_data = []
        while current_day <= last_day:
            date_for_database = current_day.strftime("%Y%m%d")
            user_habits = habits.getdata(user_id, date_for_database)
            habits_data.append(user_habits)
            current_day += timedelta(days=1)
        users_habits = habits.gethabits(user_id)
        first_day_in_database = first_day.date()
        last_day_in_database = last_day.date()
        
        habit_data_dictionary = {}
        for day in habits_data:
            for data in day:
                key = (data[2], data[3].day)
                if key not in habit_data_dictionary:
                    habit_data_dictionary[key] = []
                habit_data_dictionary[key].append(data)
        
        return render_template("month.html", month=month_date, habits=users_habits, habit_data=habit_data_dictionary, first_day=first_day_in_database, last_day=last_day_in_database)