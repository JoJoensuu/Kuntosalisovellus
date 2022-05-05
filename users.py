import secrets
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
            session["csrf_token"] = secrets.token_hex(16)
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
    del session["csrf_token"]

def get_token():
    return session.get("csrf_token",0)

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
        db.session.execute(sql, {"id":id})
        db.session.commit()
        return True
    except:
        return False

def join_gym(gym_id, user_id):
    sql = "SELECT * FROM subscriptions WHERE user_id=:user_id AND gym_id=:gym_id"
    result = db.session.execute(sql, {"user_id":user_id, "gym_id":gym_id})
    user = result.fetchall()
    if len(user) != 0:
        sql = "INSERT INTO subscriptions (user_id, gym_id, joined_at) VALUES (:user_id, :gym_id, NOW())"
        db.session.execute(sql, {"user_id":user_id, "gym_id":gym_id})
        db.session.commit()
        return True
    else:
        return False