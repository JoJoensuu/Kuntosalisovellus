import secrets
from sqlalchemy import true
from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql = "SELECT user_id, password, admin FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.user_id
            session["admin"] = user.admin
            session["csrf_token"] = secrets.token_hex(16)
            return True
        else:
            return False

def check_user(username, password):
    sql = "SELECT user_id, password, admin FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
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

def get_list(x):
    if user_id == 0:
        return False
    sql = "SELECT A.user_id, A.username, A.admin, C.name, B.joined_at FROM users as A LEFT JOIN subscriptions as B ON A.user_id=B.user_id LEFT JOIN gyms as C ON C.gym_id=B.gym_id"
    if x == 1:
        result = db.session.execute(sql)
        return result.fetchall()
    else:
        sql += " WHERE A.user_id=:user_id"
        result = db.session.execute(sql, {"user_id":user_id()})
        return result.fetchone()

def delete_user(id):
    try:
        sql = "DELETE FROM users WHERE user_id=:id"
        db.session.execute(sql, {"id":id})
        db.session.commit()
        return True
    except:
        return False

def join_gym(gym_id):
    userid = user_id()
    sql = "SELECT * FROM subscriptions WHERE user_id=:user_id"
    result = db.session.execute(sql, {"user_id":userid})
    user = result.fetchall()
    if len(user) == 0:
        sql = "INSERT INTO subscriptions (user_id, gym_id, joined_at) VALUES (:user_id, :gym_id, NOW())"
        db.session.execute(sql, {"user_id":userid, "gym_id":gym_id})
        db.session.commit()
        return True
    else:
        return False

def leave_gym(user_id):
    sql = "DELETE FROM subscriptions WHERE user_id=:user_id"
    db.session.execute(sql, {"user_id":user_id})
    db.session.commit()
    return

def change_password(pw1, pw2):
    sql = "SELECT username FROM users WHERE user_id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id()})
    user = result.fetchone()
    username = user[0]
    if not check_user(username, pw1):
        return False
    hash_value = generate_password_hash(pw2)
    sql = "UPDATE users SET password=:hash_value WHERE user_id=:user_id"
    db.session.execute(sql, {"hash_value":hash_value, "user_id":user_id()})
    db.session.commit()
    return True
