import mysql.connector
import os

def connection():
    db_connection = mysql.connector.connect(
        host="mysql-f3a7761-jevinsachaniya.e.aivencloud.com",
        port=17622, # Port add karna mat bhooliyega
        user="avnadmin",
        password=os.environ.get("AVNS_n8ebEgH6HmJqqAWQqgP"), # Seedha password yahan likhein
        database="defaultdb",
        ssl_ca=None
    )
    if db_connection.is_connected():
        # Ye line zaroori hai taaki Primary Key ka error code mein na aaye
        cursor = db_connection.cursor()
        cursor.execute("SET SESSION sql_require_primary_key = 0;")
        print("Connected to Cloud Database!")
        return db_connection

db_connection = connection()
db = db_connection.cursor()

def check_user(username):
    query = "SELECT * FROM users WHERE name = %s"
    db.execute(query, (username,))
    users = db.fetchall()
    if users:
        for member in users:
            print(f"Hello {member}...!")
            return True
    else:
        # print(f"Sorry, '{username}' naam ka koi member nahi mila!")
        return False
        
def new_user():
    table = f"""
    CREATE TABLE IF NOT EXISTS users(
        name VARCHAR(50) UNIQUE
    )
    """
    db.execute(table)
    db_connection.commit()
    print("Registeration Done...!")

def create_table(username):
    create_table = f"CREATE TABLE IF NOT EXISTS `{username}`( name VARCHAR(50) UNIQUE)"
    db.execute(create_table)
    db_connection.commit()
    
def insert(username):
    insert_qiery = f"""
    INSERT INTO {username}
    (name)
    VALUES
    (%s)
    """
    return insert_qiery 

def delete_from_user(username,bookname):
    quiry = f"DELETE FROM {username} WHERE name = %s"
    db.execute(quiry,(bookname,))
    db_connection.commit()
    

def perchase(bookname):
    quiry = "DELETE FROM books WHERE name = %s"
    db.execute(quiry,(bookname,))
    db_connection.commit()
    
def buy_or_return(bookname):
    quiry = "INSERT INTO books (name) VALUES (%s)"
    db.execute(quiry,(bookname.lower(),))
    db_connection.commit()
    
def List_Of_Books():
    quiry = "SELECT * FROM books"
    db.execute(quiry)
    books = db.fetchall()
    db_connection.commit()
    return books

def your_books(username):
    try:
        quiry = f"SELECT * FROM {username}"
        db.execute(quiry)
        your_book = db.fetchall()
        db_connection.commit()
        return your_book
    except Exception as e:
        print("No books")

def users():
    quiry = f"SELECT * FROM users"
    db.execute(quiry)
    user_list = db.fetchall()
    db_connection.commit()
    available_users = [user[0] for user in user_list]
    return available_users