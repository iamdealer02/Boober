import sqlite3
from flask import g, Flask
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()


app = Flask(__name__)

def create_user_table(db):
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin (
            user_id TEXT PRIMARY KEY,
            email TEXT ,
            password TEXT NOT NULL,
            role TEXT
        
        );          
    ''')
    db.commit()


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('./admin.db')
        create_user_table(db)
    return db

def check_user(email):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(f"SELECT * FROM ADMIN WHERE email= '{email}' ")

    data = cursor.fetchone()

    db.commit()
    
    return data

def add_user(id,email,password,role):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    db = get_db()
    cursor = db.cursor()

    cursor.execute("INSERT INTO admin (user_id, email, password,role) VALUES (?,?, ?, ?)", (id,email, hashed_password, role))

    db.commit()
    print('done')
    
    return 0

def get_admin_by_id(id):
    db = get_db()
    cursor = db.cursor()

    # Execute the SQL query to retrieve a user by ID
    cursor.execute('SELECT * FROM ADMIN WHERE user_id = ?', (id))
    user_data = cursor.fetchone()
    db.commit()
    return user_data


# if __name__ == '__main__':
#     with app.app_context():
#         add_user('ADMIN1','admin@boober.fr', '123456', 'admin')
