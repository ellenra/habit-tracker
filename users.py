import os
import re
from flask import session, request, abort
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from db import db

def register(username, email, password):
    if not username or not email or not password:
        return "Please fill in all fields!"
    if len(password) < 8:
        return "Password must be longer!"
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return "Invalid email format!"
    username_exists = db.session.execute(text("SELECT * FROM users WHERE username = :username"),
                                         {"username": username}).fetchone()
    if username_exists:
        return "Username already exists!"

    hashed_password = generate_password_hash(password)
    try:
        hashed_password = generate_password_hash(password)
        sql = text("INSERT INTO users (username, email, password) "
                   "VALUES (:username, :email, :password)")
        db.session.execute(sql, {"username":username, "email":email, "password":hashed_password})
        db.session.commit()
        user_id = db.session.execute(text("SELECT id FROM users WHERE username = :username"),
                                     {"username": username}).fetchone()[0]
        session["username"] = username
        session["user_id"] = user_id
        session["csrf_token"] = os.urandom(16).hex()
    except:
        return "Error in registration!"
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
    session["csrf_token"] = os.urandom(16).hex()
    return True

def logout():
    session.pop("user_id", None)
    session.pop("username", None)
    session.pop("csrf_token", None)

def check_csrf():
    if session.get("csrf_token") != request.form.get("csrf_token"):
        abort(403)
