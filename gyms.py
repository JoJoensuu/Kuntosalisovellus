from db import db
import users

def get_list():
    sql = "SELECT * FROM gyms WHERE visible=TRUE or visible IS NULL"
    result = db.session.execute(sql)
    return result.fetchall()

def get_reviews(id):
    sql = "SELECT * FROM reviews WHERE gym_id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

def submit(name, address, fee, description):
    admin = users.admin()
    if not admin:
        return False
    sql = "SELECT * FROM gyms WHERE name=:name"
    result = db.session.execute(sql, {"name":name})
    list = result.fetchall()
    if len(list) != 0:
        return False
    sql = "INSERT INTO gyms (name, address, fee, description, visible) VALUES (:name, :address, :fee, :description, TRUE)"
    db.session.execute(sql, {"name":name, "address":address, "fee":fee, "description":description})
    db.session.commit()
    return True

def delete_gym(id):
    try:
        sql = "UPDATE gyms SET visible=FALSE WHERE id=:id"
        result = db.session.execute(sql, {"id":id})
        db.session.commit()
        return True
    except:
        return False
