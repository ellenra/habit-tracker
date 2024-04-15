from db import db
from sqlalchemy.sql import text

def add_challenge(title, description, goal, goal_frequency, duration, start_date, end_date, color, user_id):
    sql = text("INSERT INTO Challenges (title, description, goal, goal_frequency, duration, start_date, end_date, color, creator_id) "
               "VALUES (:title, :description, :goal, :goal_frequency, :duration, :start_date, :end_date, :color, :creator_id)")
    db.session.execute(sql, {"title": title, "description": description, "goal": goal, "goal_frequency": goal_frequency,
                             "duration": duration, "start_date": start_date, "end_date": end_date, "color": color, "creator_id": user_id})
    db.session.commit()
    
def get_challenges(date):
    sql = text("SELECT * FROM Challenges WHERE end_date>:date")
    result = db.session.execute(sql, {"date": date})
    data = result.fetchall()
    return data

def join_challenge(user_id, challenge_id):
    sql = text("SELECT * FROM Userschallenges WHERE user_id=:user_id AND challenge_id=:challenge_id AND joined=:joined")
    result = db.session.execute(sql, {"user_id": user_id, "challenge_id": challenge_id, "joined": True})
    data = result.fetchone()
    if not data:
        sql_insert = text("INSERT INTO Userschallenges (user_id, challenge_id, joined) VALUES (:user_id, :challenge_id, :joined)")
        db.session.execute(sql_insert, {"user_id": user_id, "challenge_id": challenge_id, "joined": True})
        db.session.commit()
        
def leave_challenge(user_id, challenge_id):
    sql = text("UPDATE Userschallenges SET joined=:joined WHERE user_id=:user_id AND challenge_id=:challenge_id")
    db.session.execute(sql, {"joined": False, "user_id": user_id, "challenge_id": challenge_id})
    db.session.commit()
        
def get_user_challenges(user_id):
    sql = text("SELECT challenge_id FROM Userschallenges WHERE user_id=:user_id AND joined=:joined")
    result = db.session.execute(sql, {"user_id": user_id, "joined": True})
    data = result.fetchall()
    return data

def update_challenge_status(user_id, challenge_id, date):
    sql = text("SELECT * FROM UsersChallengeLogs where user_id=:user_id AND challenge_id=:challenge_id AND date=:date")
    result = db.session.execute(sql, {"user_id": user_id, "challenge_id": challenge_id, "date": date})
    data = result.fetchone()
    if not data:
        sql_insert = text("INSERT INTO UsersChallengeLogs (user_id, challenge_id, date, completed) VALUES (:user_id, :challenge_id, :date, :completed)")
        db.session.execute(sql_insert, {"user_id": user_id, "challenge_id": challenge_id, "date": date, "completed": True})
    else:
        completed = not data[4]
        sql_update = text("UPDATE UsersChallengeLogs SET completed = :completed WHERE user_id=:user_id AND challenge_id=:challenge_id AND date=:date")
        db.session.execute(sql_update, {"completed": completed, "user_id": user_id, "challenge_id": challenge_id, "date": date})
    db.session.commit()
    
def get_user_challenge_data_for_day(user_id, date):
    sql = text("SELECT challenge_id, completed FROM UsersChallengeLogs WHERE user_id=:user_id AND date=:date")
    result = db.session.execute(sql, {"user_id": user_id, "date": date})
    data = result.fetchall()
    return data

def get_challenge_frequency(challenge_id):
    sql = text("SELECT goal_frequency FROM Challenges WHERE id=:id")
    result = db.session.execute(sql, {"id": challenge_id})
    data = result.fetchone()
    return data
