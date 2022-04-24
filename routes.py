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
        if users.username_taken(username):
            return render_template("error.html", message="Username taken")
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

@app.route("/show_reviews/<int:id>")
def show_reviews(id):
    list = gyms.get_reviews(id)
    return render_template("show_reviews.html", count=len(list), reviews=list)

@app.route("/new_gym")
def new_gym():
    return render_template("new_gym.html")

@app.route("/add_gym", methods=["POST"])
def add_gym():
    if "gymname" in request.form and "gymaddress" in request.form and "gymfee" in request.form and "gymdescription" in request.form:
        name = request.form["gymname"]
        address = request.form["gymaddress"]
        fee = request.form["gymfee"]
        description = request.form["gymdescription"]
        if gyms.submit(name, address, fee, description):
            return redirect("/")
        else:
            return render_template("error.html", message="Submitting new gym failed")