from db import db
import users
from flask import session

def submit(id, stars, content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO reviews (posted_at, user_id, gym_id, stars, content) VALUES (NOW(), :user_id, :id, :stars, :content)"
    db.session.execute(sql, {"user_id":user_id, "id":id, "stars":stars, "content":content,})
    db.session.commit()    
    return True