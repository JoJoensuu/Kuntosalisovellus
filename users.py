
from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql = "SELECT id, password, admin FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["admin"] = user.admin
            return True
        else:
            return False

def register(username, password):
    hash_value = generate_password_hash(password)
    admin = False
    if username == "admin":
        admin = True
    try:
        sql = "INSERT INTO users (username,password,admin) VALUES (:username,:password,:admin)"
        db.session.execute(sql, {"username":username, "password":hash_value, "admin":admin})
        db.session.commit()
    except:
        return False
    return login(username, password)

def logout():
    del session["user_id"]
    del session["admin"]

def user_id():
    return session.get("user_id",0)

def admin():
    return session.get("admin")

def username_taken(username):
    sql = "SELECT * FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchall()
    if len(user) != 0:
        return True
    else:
        return False

def get_list():
    sql = "SELECT * FROM users"
    result = db.session.execute(sql)
    return result.fetchall()

def delete_user(id):
    try:
        sql = "DELETE FROM users WHERE id=:id"
        result = db.session.execute(sql, {"id":id})
        db.session.commit()
        return True
    except:
        return False
