from flask import Flask,redirect,render_template,url_for,flash,request,session
from database import *

app = Flask(__name__)
app.secret_key = 'Jevin@1681'

@app.route("/")
def loginpage():
    return render_template("login.html")
    
@app.route("/login", methods=["POST"])
def login_handler():
    if request.method == "POST":
        username = request.form.get("username")
        if username:
            session['user'] = username.strip()
            return redirect(url_for("homepage"))
        return redirect(url_for("loginpage"))

@app.route("/home" , methods = ["POST","GET"])
def homepage():
    username = session.get('user')
    if 'user' not in session:
        return redirect(url_for("loginpage"))
    return render_template("home.html", username=username)

@app.route("/see-books", methods = ["POST","GET"])
def seeAvailableBooks():
    username = session.get('user')
    if 'user' not in session:
        return redirect(url_for("loginpage"))
    
    book_list = List_Of_Books() or []
    return render_template("see_book.html", book_list = book_list, username = username)
    
@app.route("/buy-book-page", methods = ["POST","GET"])
def buyBookpage():
    username = session.get('user')
    if 'user' not in session:
        return redirect(url_for("loginpage"))
    book_list = List_Of_Books()
    return render_template("buy.html",book_list = book_list,username=username)

@app.route("/buy-book", methods = ["POST","GET"])
def buyBook():
    if request.method == "POST":
        bookName = request.form.get("buy-book")
        username = session.get('user')
        
        if 'user' not in session:
            return redirect(url_for("loginpage"))
        
        row_books = List_Of_Books()
        clear_book_name = bookName.strip().lower()
        available_books = [book[0].lower().strip() for book in row_books]
        if clear_book_name not in available_books:
            print(f"Sorry, {clear_book_name} is not available.")
        else:
            try:
                create_table(username)          
                sql_query = insert(username)
                db.execute(sql_query, (clear_book_name,))
                db_connection.commit()
                perchase(clear_book_name)
                print(f"Success! You bought {clear_book_name}")
            except Exception as e:
                print(e)     
        return redirect(url_for("homepage"))
                
                
@app.route("/return-book-page",  methods = ["POST","GET"])
def returnbookpage():
    if request.method == "POST":
        username = session.get('user')
        
        if 'user' not in session:
            return redirect(url_for("loginpage"))
        
        my_books = your_books(username)
        print(f"\n------- {username} Your Books --------\n")
        return render_template("return.html", my_books = my_books,username = username)

@app.route("/return-book", methods=["POST","GET"])
def returnBook():
    if request.method == "POST":
        bookName = request.form.get("return-book")
        username = session.get('user')
        
        if 'user' not in session:
            return redirect(url_for("loginpage"))
        
        clear_book_name = bookName.strip().lower()
        user_books = your_books(username)
        available_books = [book[0].lower().strip() for book in user_books]
        if clear_book_name not in available_books:
            print("Please Enter Valid Book Name")
        else:
            delete_from_user(username,clear_book_name)
            buy_or_return(clear_book_name)
            print(f"You Return {clear_book_name}. I Hope You Enjoy...!")
            
        return redirect(url_for("homepage"))
    
@app.route("/your-books", methods=["POST","GET"])
def yourbooks():
    username = session.get('user')
    
    if 'user' not in session:
        return redirect(url_for("loginpage"))
    
    my_books = your_books(username) or []
    print(f"\n------- {username} Your Books --------\n")
    return render_template("see_user_books.html", my_books = my_books, username = username)

@app.route("/donate-book-page", methods=["POST","GET"])
def donatebookpage():
    username = session.get('user')
    
    if 'user' not in session:
        return redirect(url_for("loginpage"))
    
    return render_template("donate.html",username = username)

@app.route("/donate-book", methods=["POST","GET"])
def donatebook():
    if request.method == "POST":
        bookname = request.form.get("donate-book")
        buy_or_return(bookname)
        return redirect(url_for("homepage"))
    

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('loginpage'))

if __name__ == "__main__":
    app.run(debug = True)