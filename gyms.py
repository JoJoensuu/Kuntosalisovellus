from db import db
import users

def get_reviews(id):
    sql = "SELECT * FROM reviews WHERE gym_id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

def submit(name, address, fee, description, type_id):
    admin = users.admin()
    if not admin:
        return False
    sql = "SELECT * FROM gyms WHERE name=:name"
    result = db.session.execute(sql, {"name":name})
    list = result.fetchall()
    if len(list) != 0:
        return False
    sql = "INSERT INTO gyms (name, address, fee, description, visible, type_id) VALUES (:name, :address, :fee, :description, TRUE, :type_id)"
    db.session.execute(sql, {"name":name, "address":address, "fee":fee, "description":description, "type_id":type_id})
    db.session.commit()
    return True

def delete_gym(id):
    try:
        sql = "UPDATE gyms SET visible=FALSE WHERE gym_id=:id"
        db.session.execute(sql, {"id":id})
        db.session.commit()
        return True
    except:
        return False

def get_info(id):
    sql = "SELECT gyms.name, gyms.address, gyms.fee, gyms.description, gym_types.name, gyms.gym_id FROM gyms LEFT JOIN gym_types ON gyms.type_id=gym_types.type_id WHERE gyms.gym_id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

def alter(id, name, address, fee, description, gym_type):
    admin = users.admin()
    if not admin:
        return False
    try:
        sql = "UPDATE gyms SET name=:name, address=:address, fee=:fee, description=:description, type_id=:gym_type WHERE gym_id=:id"
        db.session.execute(sql, {"name":name, "address":address, "fee":fee, "description":description, "gym_type":gym_type, "id":id})
        db.session.commit()
        return True
    except:
        return False

def search(name, address, price1, price2, sort):
    if price1 == "":
        price1 = "0"
    if price2 == "":
        price2 = "9999"
    sql = "SELECT gym_id, name, fee FROM gyms WHERE visible=TRUE or visible IS NULL AND name LIKE :name AND address LIKE :address AND fee BETWEEN :price1 AND :price2"
    if sort == "1":
        sql += " ORDER BY fee"
    else:
        sql += " ORDER BY name"
    result = db.session.execute(sql, {"name":"%"+name+"%", "address":"%"+address+"%", "price1":price1, "price2":price2})
    return result.fetchall()
