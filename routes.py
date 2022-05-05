from app import app
from flask import render_template, request, redirect
import users, gyms, reviews

@app.route("/")
def index():
    list = gyms.get_list()
    sum = gyms.get_sum()
    return render_template("index.html", count=sum[0], gyms=list)

@app.route("/show_users")
def show_users():
    list = users.get_list()
    return render_template("users.html", count=len(list), users=list)

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
        if not username:
            return render_template("error.html", message="No username given")
        if not password1:
            return render_template("error.html", message="Password cannot be empty")
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
    sum = reviews.get_sum(id)
    return render_template("show_reviews.html", count=sum[0], reviews=list)

@app.route("/new_gym")
def new_gym():
    return render_template("new_gym.html")

@app.route("/add_gym", methods=["POST"])
def add_gym():
    if "gymname" in request.form and "gymaddress" in request.form and "gymfee" in request.form and "gymdescription" in request.form and "gymtype" in request.form:
        name = request.form["gymname"]
        address = request.form["gymaddress"]
        fee = request.form["gymfee"]
        description = request.form["gymdescription"]
        gym_type = request.form["gymtype"]
        if gyms.submit(name, address, fee, description, gym_type):
            return redirect("/")
        else:
            return render_template("error.html", message="Submitting new gym failed")

@app.route("/delete_gym/<int:id>")
def delete_gym(id):
    if gyms.delete_gym(id):
        return redirect("/")
    else:
        return render_template("error.html", message="Gym deletion failed")

@app.route("/remove_user/<int:id>")
def remove_user(id):
    if users.delete_user(id):
        return redirect("/show_users")
    else:
        return render_template("error.html", message="User deletion failed")

@app.route("/remove_review/<int:id>")
def remove_review(id):
    if reviews.delete_review(id):
        return redirect("/")
    else:
        return render_template("error.html", message="Review deletion failed")

@app.route("/gym_info/<int:id>")
def gym_info(id):
    info = gyms.get_info(id)
    return render_template("gym_info.html", gym=info)

@app.route("/modify_gym/<int:id>")
def modify_gym(id):
    info = gyms.get_info(id)
    return render_template("modify_gym.html", id=id, gym=info)

@app.route("/save_changes", methods=["POST"])
def save_changes():
    gym_id = request.form["id"]
    name = request.form["gymname"]
    address = request.form["gymaddress"]
    fee = request.form["gymfee"]
    description = request.form["gymdescription"]
    gym_type = request.form["gymtype"]
    if gyms.alter(gym_id, name, address, fee, description, gym_type):
        return redirect("/")
    else:
        return render_template("error.html", message="Modifying gym info failed")

@app.route("/gotosearch")
def gotosearch():
    return render_template("search.html")

@app.route("/search", methods=["GET"])
def search_gyms():
    query = request.args["query"]
    list = gyms.search(query)
    return render_template("search.html", gyms=list)
