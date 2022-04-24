from app import app
from flask import render_template, request, redirect
import users, gyms, reviews

@app.route("/")
def index():
    list = gyms.get_list()
    return render_template("index.html", count=len(list), gyms=list)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username and users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Wrong username or password")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Passwords don't match")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Failed to register user")


@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/new_review/<int:id>")
def new_review(id):
    return render_template("new.html", id=id)

@app.route("/submit_review", methods=["POST"])
def submit_review():
    gym_id = request.form["id"]
    if "content" in request.form:
        stars = request.form["stars"]
        content = request.form["content"]
        if reviews.submit(gym_id, stars, content):
            return redirect("/")
        else:
            return render_template("error.html", message="Submitting the review failed")