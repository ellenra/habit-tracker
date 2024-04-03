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

def getdata(user_id, date):
    sql = text("SELECT * FROM Usershabits WHERE user_id=:user_id AND date=:date")
    result = db.session.execute(sql, {"user_id": user_id, "date": date})
    data = result.fetchall()
    print(data)
    return data

def get_form_status(date):
    sql = text("SELECT * FROM Usershabits WHERE date=:date AND form_submitted = TRUE")
    result = db.session.execute(sql, {"date":date})
    status = result.fetchone()
    if status:
        return True
    else:
        return None

def add_habits_for_the_day(user_id, date):
    sql = text("SELECT * FROM Usershabits WHERE user_id=:user_id AND date=:date")
    result = db.session.execute(sql, {"user_id":user_id, "date":date})
    existing_data = result.fetchone()
    if existing_data is None:
        sql_get_habits = text("SELECT id, habit_name, track_number_value FROM Habits WHERE user_id=:user_id")
        data = db.session.execute(sql_get_habits, {"user_id":user_id})
        habits = data.fetchall()
        for habit in habits:
            habit_id, habit_name, track_number_value = habit
            sql_add_habit = text("INSERT INTO UsersHabits (user_id, habit_id, habit_name, date, track_number_value) "
                                 "VALUES (:user_id, :habit_id, :habit_name, :date, :track_number_value)")
            db.session.execute(sql_add_habit, {"user_id": user_id, "habit_id": habit_id, "habit_name": habit_name,
                                                "date": date, "track_number_value": track_number_value})
    db.session.commit()

    
def update_habit_number_value(habit_id, value):
    sql = text("UPDATE Usershabits SET number_value=:value WHERE id=:habit_id")
    db.session.execute(sql, {"value":value, "habit_id":habit_id})
    sql_update_status = text("UPDATE Usershabits SET form_submitted = TRUE WHERE id=:habit_id")
    db.session.execute(sql_update_status, {"habit_id":habit_id})
    db.session.commit()
    
def update_habit_boolean_value(habit_id):
    update_sql = text("UPDATE Usershabits SET boolean_value = TRUE WHERE id=:habit_id")
    db.session.execute(update_sql, { "habit_id":habit_id})
    sql_update_status = text("UPDATE Usershabits SET form_submitted = TRUE WHERE id=:habit_id")
    db.session.execute(sql_update_status, {"habit_id":habit_id})
    db.session.commit()
    
