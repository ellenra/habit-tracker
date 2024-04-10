from db import db
import re
from flask import session
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash

def register(username, email, password):
    if not username or not email or not password:
        return False
    if len(password) < 6:
        return False
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False
    username_exists = db.session.execute(text("SELECT * FROM users WHERE username = :username"), {"username": username}).fetchone()
    if username_exists:
        return False
    hashed_password = generate_password_hash(password)
    try:
        hashed_password = generate_password_hash(password)
        sql = text("INSERT INTO users (username, email, password) VALUES (:username, :email, :password)")
        db.session.execute(sql, {"username":username, "email":email, "password":hashed_password})
        db.session.commit()
        user_id = db.session.execute(text("SELECT id FROM users WHERE username = :username"), {"username": username}).fetchone()[0]
        session["username"] = username
        session["user_id"] = user_id
    except:
        return False
    return True

def login(username, password):
    sql = text("SELECT password, id FROM Users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    if not check_password_hash(user[0], password):
        return False
    session["username"] = username
    session["user_id"] = user[1]
    return True

def logout():
    del session["username"]
    del session["user_id"]


