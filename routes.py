from app import app
from flask import render_template, request, redirect
import users, gyms, reviews

# MAIN PAGE, LOGIN, LOGOUT AND REGISTERING A NEW USER
@app.route("/")
def index():
    return render_template("index.html")

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
            return render_template("error.html",
                message="Wrong username or password")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if not username:
            return render_template("error.html",
                message="No username given")
        if not password1:
            return render_template("error.html",
                message="Password cannot be empty")
        if users.username_taken(username):
            return render_template("error.html",
                message="Username taken")
        if password1 != password2:
            return render_template("error.html",
                message="Passwords don't match")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html",
                message="Failed to register user")

# ADMIN FUNCTIONALITIES

@app.route("/show_users")
def show_users():
    list = users.get_list(1)
    return render_template("users.html",
        count=len(list), users=list)

@app.route("/new_gym")
def new_gym():
    return render_template("new_gym.html")

@app.route("/add_gym", methods=["POST"])
def add_gym():
    if users.get_token() != request.form["token"]:
        return render_template("error.html",
            message="Invalid session token")
    if ("gymname" in request.form
            and "gymaddress" in request.form
            and "gymfee" in request.form
            and "gymdescription" in request.form
            and "gymtype" in request.form):
        name = request.form["gymname"]
        address = request.form["gymaddress"]
        fee = request.form["gymfee"]
        if not int(fee) or int(fee) < 0 or int(fee) > 9999:
            return render_template("error.html",
            message="Fee has to be a value between 1 and 9999")
        description = request.form["gymdescription"]
        gym_type = request.form["gymtype"]
        if gyms.submit(name, address, fee, description, gym_type):
                return redirect("/")
        else:
            return render_template("error.html",
                message="Submitting new gym failed")

@app.route("/modify_gym/<int:id>")
def modify_gym(id):
    info = gyms.get_info(id)
    return render_template("modify_gym.html", id=id, gym=info)

@app.route("/save_changes", methods=["POST"])
def save_changes():
    if users.get_token() != request.form["token"]:
        return render_template("error.html",
            message="Invalid session token")
    gym_id = request.form["id"]
    name = request.form["gymname"]
    address = request.form["gymaddress"]
    fee = request.form["gymfee"]
    description = request.form["gymdescription"]
    gym_type = request.form["gymtype"]
    if gyms.alter(gym_id, name, address, fee,
            description, gym_type):
        return redirect("/")
    else:
        return render_template("error.html",
            message="Modifying gym info failed")

@app.route("/delete_gym/<int:id>")
def delete_gym(id):
    if gyms.delete_gym(id):
        return redirect("/")
    else:
        return render_template("error.html",
            message="Gym deletion failed")

@app.route("/remove_user/<int:id>")
def remove_user(id):
    if users.delete_user(id):
        return redirect("/show_users")
    else:
        return render_template("error.html",
            message="User deletion failed")

@app.route("/remove_review/<int:id>")
def remove_review(id):
    if reviews.delete_review(id):
        return redirect("/")
    else:
        return render_template("error.html",
            message="Review deletion failed")

# NORMAL USER FUNCTIONALITIES

@app.route("/password")
def password():
    return render_template("change_password.html")

@app.route("/change_password", methods=["POST"])
def change_password():
    if users.get_token() != request.form["token"]:
        return render_template("error.html",
            message="Invalid session token")
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    password3 = request.form["password3"]
    if not password1:
        return render_template("error.html",
            message="All the fields must be filled")
    if not password2:
        return render_template("error.html",
            message="All the fields must be filled")
    if password2 != password3:
        return render_template("error.html",
            message="Passwords don't match")
    if password1 == password2:
        return render_template("error.html",
            message="New password cannot be same as old password")
    if users.change_password(password1, password2):
        return redirect("/")
    else:
        return render_template("error.html",
            message="Failed to change password")

@app.route("/user_info")
def user_info():
    info = users.get_list(2)
    return render_template("user_info.html", user=info)

@app.route("/gotosearch")
def gotosearch():
    return render_template("search.html")

@app.route("/search", methods=["GET"])
def search_gyms():
    name = request.args["name"]
    address = request.args["address"]
    price1 = request.args["price1"]
    price2 = request.args["price2"]
    sort = request.args["sort"]
    list = gyms.search(name, address, price1, price2, sort)
    return render_template("search.html",
        gyms=list, count=len(list))

@app.route("/gym_info/<int:id>")
def gym_info(id):
    info = gyms.get_info(id)
    return render_template("gym_info.html", gym=info)

@app.route("/new_review/<int:id>")
def new_review(id):
    return render_template("new_review.html", id=id)

@app.route("/submit_review", methods=["POST"])
def submit_review():
    if users.get_token() != request.form["token"]:
        return render_template("error.html",
            message="Invalid session token")
    gym_id = request.form["id"]
    if "content" in request.form:
        stars = request.form["stars"]
        content = request.form["content"]
        if reviews.submit(gym_id, stars, content):
            return redirect("/gotosearch")
        else:
            return render_template("error.html",
                message="Submitting the review failed")

@app.route("/show_reviews/<int:id>")
def show_reviews(id):
    list = gyms.get_reviews(id)
    sum = reviews.get_sum(id)
    return render_template("show_reviews.html",
        count=sum[0], reviews=list)

@app.route("/join_gym/<int:id>")
def join_gym(id):
    info = gyms.get_info(id)
    return render_template("subscribe.html", id=id, gym=info)

@app.route("/subscribe", methods=["POST"])
def subscribe():
    if users.get_token() != request.form["token"]:
        return render_template("error.html",
            message="Invalid session token")
    gym_id = request.form["gym_id"]
    if users.join_gym(gym_id):
        return redirect("/")
    else:
        return render_template("error.html", message="FAILED")

@app.route("/cancel_subscription/<int:id>", methods=["POST"])
def unsubscribe(id):
    if users.get_token() != request.form["token"]:
        return render_template("error.html",
            message="Invalid session token")
    users.leave_gym(id)
    return redirect("/")
