#from flaskblog.models import user, post
from datetime import datetime
from . import mysql

# --- Post functions ---

def get_posts():
    cur = mysql.connection.cursor()
    cur.execute("SELECT title, content, date_posted FROM post")
    posts = cur.fetchall()
    cur.close()
    return [Post(str(row[0]), row[1], row[2]) for row in posts]

def get_post(title):
    cur = mysql.connection.cursor()
    cur.execute("SELECT title, content, date_posted FROM post WHERE title = %s", (title,))
    row = cur.fetchone()
    cur.close()
    if row:
        return Title(str(row[0]), row[1], row[2])
    return None

def add_post(title, content):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO post (title, content, date_posted) VALUES (%s, %s, %s)", (title, content, datetime.now()))
    mysql.connection.commit()
    cur.close()


# --- User functions ---
def add_user(username, email, password):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO user (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
    mysql.connection.commit()
    cur.close()

def get_user_by_email(email, password):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT user_id, username, email, password 
        FROM user 
        WHERE email = %s AND password = %s
                """, (email, password))
    row = cur.fetchone()
    cur.close()
    if row:
        return {
            'user_id': row[0],
            'username': row[1],
            'email': row[2],
            'password': row[3]
        }
    return None

def check_for_user(email, password):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user WHERE email = %s AND password = %s", (email, password))
    row = cur.fetchone()
    cur.close() 
    if row:
        return UserAccount(row['username'], row['email'], row['password'])
    return None
