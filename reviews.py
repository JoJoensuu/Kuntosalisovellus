from db import db
import users
from flask import session

def submit(id, stars, content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "SELECT * FROM reviews WHERE user_id=:userid AND gym_id=:id"
    result = db.session.execute(sql, {"userid":user_id, "id":id})
    list = result.fetchall()
    if len(list) != 0:
        return False
    sql = "INSERT INTO reviews (posted_at, user_id, gym_id, stars, comment) VALUES (NOW(), :user_id, :id, :stars, :comment)"
    db.session.execute(sql, {"user_id":user_id, "id":id, "stars":stars, "comment":content,})
    db.session.commit()    
    return True

def delete_review(id):
    try:
        sql = "DELETE FROM reviews WHERE review_id=:id"
        result = db.session.execute(sql, {"id":id})
        db.session.commit()
        return True
    except:
        return False

def get_sum(id):
    sql = "SELECT COUNT(reviews) FROM reviews LEFT JOIN gyms ON reviews.gym_id=gyms.id WHERE reviews.gym_id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()
