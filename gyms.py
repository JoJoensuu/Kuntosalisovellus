from db import db
import users

def get_list():
    sql = "SELECT * FROM gyms"
    result = db.session.execute(sql)
    return result.fetchall()

def get_reviews(id):
    sql = "SELECT * FROM reviews WHERE gym_id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()
