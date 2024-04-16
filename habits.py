from db import db
from sqlalchemy.sql import text

def addhabits(sleep, workout, steps, study, journal, meditate, mood, user_id):
    habits = {
        'sleep': sleep,
        'workout': workout,
        'steps': steps,
        'study': study,
        'journal': journal,
        'meditate': meditate,
        'mood': mood
    }
    
    for name, value in habits.items():
        if value == 'true':
            if name == 'sleep' or name == 'steps' or name == 'mood':
                sql = text("INSERT INTO Habits (habit_name, user_id, track_number_value) VALUES (:habit_name, :user_id, :track_number_value)")
                db.session.execute(sql, {"habit_name":name, "user_id":user_id, "track_number_value":True})
            else:
                sql = text("INSERT INTO Habits (habit_name, user_id, track_number_value) VALUES (:habit_name, :user_id, :track_number_value)")
                db.session.execute(sql, {"habit_name":name, "user_id":user_id, "track_number_value":False})
    db.session.commit()
    
def gethabits(user_id):
    sql = text("SELECT * FROM Habits WHERE user_id=:user_id")
    result = db.session.execute(sql, {"user_id": user_id})
    data = result.fetchall()
    habits = [row[1] for row in data]
    return habits

def delete_habits(user_id):
    sql = text("DELETE FROM Habits WHERE user_id=:user_id")
    db.session.execute(sql, {"user_id":user_id})
    db.session.commit()
    
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
    sql = text("SELECT * FROM Usershabits WHERE date=:date AND form_submitted = TRUE AND user_id=:user_id")
    result = db.session.execute(sql, {"date":date, "user_id":user_id})
    data = result.fetchone()
    if data:
        return True
    return None

def add_habits_for_the_day(user_id, date):
    sql = text("SELECT * FROM Usershabits WHERE user_id=:user_id AND date=:date")
    result = db.session.execute(sql, {"user_id":user_id, "date":date})
    existing_data = result.fetchone()
    if existing_data is None:
        sql_get_habits = text("SELECT habit_name, track_number_value FROM Habits WHERE user_id=:user_id")
        data = db.session.execute(sql_get_habits, {"user_id":user_id})
        habits = data.fetchall()
        for habit in habits:
            habit_name, track_number_value = habit
            sql_add_habit = text("INSERT INTO UsersHabits (user_id, habit_name, date, track_number_value) "
                                 "VALUES (:user_id, :habit_name, :date, :track_number_value)")
            db.session.execute(sql_add_habit, {"user_id": user_id, "habit_name": habit_name,
                                                "date": date, "track_number_value": track_number_value})
    db.session.commit()

def update_habit_number_value(id, value):
    sql = text("UPDATE Usershabits SET number_value=:value WHERE id=:id")
    db.session.execute(sql, {"value":value, "id":id})
    sql_update_status = text("UPDATE Usershabits SET form_submitted = TRUE WHERE id=:id")
    db.session.execute(sql_update_status, {"id":id})
    db.session.commit()
    
def update_habit_boolean_value(id, info):
    sql_get_value = text("SELECT boolean_value FROM Usershabits WHERE id=:id")
    result = db.session.execute(sql_get_value, {"id": id})
    value = result.fetchone()[0]
    if info == True:
        new_value = not value if value is not None else True
    else:
        new_value = False
    sql_update = text("UPDATE Usershabits SET boolean_value=:new_value WHERE id=:id")
    db.session.execute(sql_update, {"new_value":new_value, "id":id})
    sql_update_status = text("UPDATE Usershabits SET form_submitted = TRUE WHERE id=:id")
    db.session.execute(sql_update_status, {"id":id})
    db.session.commit()
    
