from sqlalchemy.sql import text
from db import db

def addhabits(sleep, workout, steps, study, journal, meditate, mood, user_id):
    habits = {
        "sleep": sleep,
        "workout": workout,
        "steps": steps,
        "study": study,
        "journal": journal,
        "meditate": meditate,
        "mood": mood
    }

    for name, value in habits.items():
        if value == "true":
            if name in ("sleep", "steps", "mood"):
                sql = text("INSERT INTO Habits (habit_name, user_id, track_number_value) "
                           "VALUES (:habit_name, :user_id, :track_number_value)")
                db.session.execute(sql, {"habit_name":name, "user_id":user_id,
                                         "track_number_value":True})
            else:
                sql = text("INSERT INTO Habits (habit_name, user_id, track_number_value) "
                           "VALUES (:habit_name, :user_id, :track_number_value)")
                db.session.execute(sql, {"habit_name":name, "user_id":user_id,
                                         "track_number_value":False})
    db.session.commit()

def gethabits(user_id):
    sql = text("SELECT id, habit_name FROM Habits WHERE user_id=:user_id")
    result = db.session.execute(sql, {"user_id": user_id})
    habits = result.fetchall()
    return habits

def delete_data(user_id, date):
    sql = text("DELETE FROM Usershabits WHERE user_id=:user_id AND date>=:date")
    db.session.execute(sql, {"user_id":user_id, "date":date})
    db.session.commit()

def getdata(user_id, date):
    sql = text("SELECT * FROM Usershabits WHERE user_id=:user_id AND date=:date")
    result = db.session.execute(sql, {"user_id": user_id, "date": date})
    data = result.fetchall()
    return data

def get_form_status(date, user_id):
    sql = text("SELECT * FROM Usershabits "
               "WHERE date=:date AND form_submitted = TRUE AND user_id=:user_id")
    result = db.session.execute(sql, {"date":date, "user_id":user_id})
    data = result.fetchone()
    if data:
        return True
    return None

def add_habits_for_the_day(user_id, date, update_status):
    sql = text("SELECT * FROM Usershabits WHERE user_id=:user_id AND date=:date")
    result = db.session.execute(sql, {"user_id":user_id, "date":date})
    existing_data = result.fetchone()
    if existing_data is None or update_status:
        sql_get_habits = text("SELECT habit_name, track_number_value "
                              "FROM Habits WHERE user_id=:user_id")
        data = db.session.execute(sql_get_habits, {"user_id":user_id})
        habits = data.fetchall()

        existing_habits = []
        sql_get_existing_habits = text("SELECT habit_name FROM UsersHabits "
                                   "WHERE user_id=:user_id AND date=:date")
        existing_data = db.session.execute(sql_get_existing_habits, {"user_id": user_id, "date": date})
        for habit_name in existing_data.fetchall():
            existing_habits.append(habit_name[0])

        for habit in habits:
            habit_name, track_number_value = habit
            if habit_name not in existing_habits:
                sql_add_habit = text("INSERT INTO UsersHabits "
                                    "(user_id, habit_name, date, track_number_value) "
                                    "VALUES (:user_id, :habit_name, :date, :track_number_value)")
                db.session.execute(sql_add_habit, {"user_id": user_id,
                                                "habit_name": habit_name,
                                                "date": date,
                                                "track_number_value": track_number_value})
    db.session.commit()

def update_habit_number_value(habit_id, value):
    sql = text("UPDATE Usershabits SET number_value=:value WHERE id=:id")
    db.session.execute(sql, {"value":value, "id":habit_id})
    sql_update_status = text("UPDATE Usershabits SET form_submitted = TRUE WHERE id=:id")
    db.session.execute(sql_update_status, {"id":habit_id})
    db.session.commit()

def update_habit_boolean_value(habit_id, info):
    sql_get_value = text("SELECT boolean_value FROM Usershabits WHERE id=:id")
    result = db.session.execute(sql_get_value, {"id": habit_id})
    value = result.fetchone()[0]
    if info is True:
        new_value = not value if value is not None else True
    else:
        new_value = False
    sql_update = text("UPDATE Usershabits SET boolean_value=:new_value WHERE id=:id")
    db.session.execute(sql_update, {"new_value":new_value, "id":habit_id})
    sql_update_status = text("UPDATE Usershabits SET form_submitted = TRUE WHERE id=:id")
    db.session.execute(sql_update_status, {"id":habit_id})
    db.session.commit()
    
def add_custom_habit(habit_name, user_id, tracking_type):
    if tracking_type == "number":
        sql = text("INSERT INTO Habits (habit_name, user_id, track_number_value) "
                    "VALUES (:habit_name, :user_id, :track_number_value)")
        db.session.execute(sql, {"habit_name":habit_name, "user_id":user_id,
                                    "track_number_value":True})
    else:
        sql = text("INSERT INTO Habits (habit_name, user_id, track_number_value) "
                    "VALUES (:habit_name, :user_id, :track_number_value)")
        db.session.execute(sql, {"habit_name":habit_name, "user_id":user_id,
                                    "track_number_value":False})
    db.session.commit()

def delete_habit(user_id, id):
    sql = text("DELETE FROM Habits WHERE user_id=:user_id AND id=:id")
    db.session.execute(sql, {"user_id":user_id, "id":id})
    db.session.commit()