from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    # todo check username and password
    session["username"] = username
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/write_review/<int:id>")
def write_review(id):
    return render_template("new_review.html")

@app.route("/submit", methods=["POST"])
def submit():
    gym_id = request.form["id"]
    if "stars" in request.form and "review" in request.form:
        stars = request.form["stars"]
        review = request.form["review"]
        sql = "INSERT INTO reviews (posted_at, gym_id, stars, comment) VALUES (NOW(), :gym_id, :stars, :review)"
        db.session.execute(sql, {"gym_id":gym_id, "stars":stars, "review":review})
        db.session.commit()
    return redirect("/reviews/" + str(gym_id))

@app.route("/show_reviews/<int:id>")
def show_reviews(id):
    sql = "SELECT name FROM gyms WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    gym = result.fetchone()[0]
    sql = "SELECT reviews.user_id, reviews.stars, reviews.comment FROM gyms LEFT JOIN reviews ON gyms.id=reviews.gym_id"
    result = db.session.execute(sql)
    reviews = result.fetchall()
    return render_template("show_reviews.html", gym=gym, reviews=reviews)