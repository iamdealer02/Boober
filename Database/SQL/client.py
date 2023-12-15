import sqlite3
from flask import g 

def create_user_table(db):
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT ,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        );          
    ''')
    db.commit()

def get_db():
    db  = getattr(g, '_database', None )
    if db is None:
        db = g._database = sqlite3.connect('./user.db')
        create_user_table(db)
    return db

def add_user(email,password,role):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("INSERT INTO users (email, password, role) VALUES (?, ?,?)", (email, password,role))

    db.commit()
    print('done')
    
    return 0

def check_user(email):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(f"SELECT * FROM USERS WHERE email= '{email}' ")

    data = cursor.fetchone()

    db.commit()
    
    return data

def is_email_taken(email):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(f"SELECT email FROM users where email= '{email}'")

    result = cursor.fetchone()

    db.commit()
    return result is not None

def get_user_by_id(user_id):
    db = get_db()
    cursor = db.cursor()

    # Execute the SQL query to retrieve a user by ID
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user_data = cursor.fetchone()
    db.commit()
    return user_data


# ---------------------------------------------------------------------------------------------------------------------------------------------
