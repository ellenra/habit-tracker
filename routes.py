from app import app
from db import db
from flask import render_template, request, session, redirect
import users

@app.route("/")
def index():
    return render_template("index.html")

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
        return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if not users.login(username, password):
        return render_template("index.html", notification=True, message="Log in failed!")
    return redirect("/")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")