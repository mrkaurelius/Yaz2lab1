from flask import Flask
from sqlalchemy.sql import text
from sqlalchemy import create_engine

from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask import jsonify
from uuid import uuid1

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

from imprc import readisbn
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'such secret'    
#app.config['UPLOAD_FOLDER'] = './uploads'

engine = create_engine('postgresql+psycopg2://mrk0:qazwsxedc@localhost/yazlab3')

# TODO: 
# build basic mechanism for chehcing auth
@app.route('/')
def home():
    # TODO:
    # if user logged in redirect /user
    # if admin logged in redirect /admin
    return render_template('home.html')

@app.route('/admin')
# admin root
def admin_root():
    # TODO: print arttime
    return render_template('admin.html')

@app.route('/admin/login', methods=('GET', 'POST'))
# do admin login
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        con = engine.connect()
        # come and hack me I insist :)
        # TODO: do secure binding
        sql_string = 'select * from users where username = ' + "'" + (username) +  "'"
        user = con.execute(sql_string).fetchone()

        error = None
        # user = db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['passwdsha256'], password):
            error = 'Incorrect password.'
        elif user['user_role'] == 1:
            error = 'You have no power here!'
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['username'] = username
            #flash("haluya giris yaptın" + username)
            return redirect('/admin')
        flash(error)

    return render_template('login.html')
    #return 'adminlogin'

@app.route('/admin/logout')
def admin_logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("home"))
    #return 'adminlogout'    

@app.route('/admin/addbook',methods=('GET', 'POST'))
# TODO: check if user admin
def add_book():
    if request.method == 'POST':
        f = request.files['file']
        f_extension = f.filename.split(".")[-1]
        f.filename = uuid1().__str__() + "." + f_extension
        f.save('./uploads/' + secure_filename(f.filename))
        booktitle = request.form['title']        
        isbn = readisbn(f.filename)
        if isbn is None:
            # pass info about upload status
            return render_template('addbook.html', books = list_books_db())
        else:
            # pass info about upload status
            addbook_db(booktitle,isbn,f.filename)
            return render_template('addbook.html', books = list_books_db())

    return render_template('addbook.html', books = list_books_db())

@app.route('/admin/forwardtime')
def forward_time():
    # redundant redirect
    # get arttime increase timestamp and change arttime
    sql_string = 'SELECT timeis FROM arttime ORDER BY timeis DESC LIMIT 1'
    con = engine.connect()
    arttime = con.execute(sql_string).fetchone()['timeis']
    #print(arttime)
    new_arttime = arttime + datetime.timedelta(days=20)
    #print(new_arttime)
    sql_string = "INSERT INTO arttime (timeis) VALUES( '"+ str(new_arttime) +"')"
    con.execute(sql_string)
    return redirect(url_for('admin_root'))
 
@app.route('/admin/listuser')
# list borrowed books also
def list_user():
    return render_template('listuser.html', users = list_users_db())

@app.route('/user')
# user root
def user_root():
    # TODO:
    # check user logged
    borrowed_books = list_borrowed_books_db(session['username'])
    print(borrowed_books)
    return render_template('user.html',username = session['username'], borrowed_books = borrowed_books )

@app.route('/user/login', methods=('GET', 'POST'))
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        con = engine.connect()
        # come and hack me I insist :)
        # TODO: do secure binding
        sql_string = 'select * from users where username = ' + "'" + (username) +  "'"
        user = con.execute(sql_string).fetchone()
        error = None
        # user = db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['passwdsha256'], password):
            error = 'Incorrect password.'
        elif user['user_role'] == 0:
            error = 'You are overqualified!'            
        # check is user over qualified
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['username'] = username
            #flash("haluya giris yaptın" + username)
            return redirect('/user')
        flash(error)

    return render_template('login.html')

@app.route('/user/logout')
def user_logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("home"))

@app.route('/user/querybook', methods=('GET', 'POST'))
# TODO:
# list only available books
def query_book():
    if request.method == 'POST':
        # handle form data
        # check isbn or title 
        print("debug",request.form['isbn'])
        if len(request.form['isbn']) == 0  and isinstance(request.form['title'], str):
            return render_template('querybook.html', books = list_book_by_title_db(request.form['title']))
        # 9789754589276
        elif len(request.form['title']) == 0  and isinstance(request.form['isbn'], str):
            return render_template('querybook.html', books = list_book_by_isbn_db(request.form['isbn']))
        else:
            render_template('querybook.html')

    return render_template('querybook.html')

@app.route('/user/borrowbook', methods=('GET', 'POST'))
# BURADA KALDIM
# TODO:
# check borrowing available
# check book available
# print errors
def borrow_book():
    borrowed_books = list_borrowed_books_db(session['username'])
    if request.method == "POST":
        # evaluate form data
        pass
        
        render_template('borrowbook.html', borrowed_books = borrowed_books)

    return render_template('borrowbook.html', borrowed_books = borrowed_books)  

@app.route('/user/returnbook')
def return_book():
    return 'returnbook'  

def check_book_available(bookname):
    # give book according to title not isbn, id handle problems
    pass

def check_user_permitted(username):
    # check user book count
    pass

####################################################################################

@app.route('/json/books')
def getallbooks():
    # pythonic way to do 
    ret = []
    with engine.connect() as con:
        rows = con.execute("select * from books")
        for row in rows:
            ret.append(dict(row))
    return jsonify(ret)

@app.route('/json/users')
def getallusers():
    # pythonic way to do 
    ret = []
    with engine.connect() as con:
        rows = con.execute("select * from users")
        for row in rows:
            ret.append(dict(row))
    return jsonify(ret) 

@app.route('/json/borrowedbooks')
def getallborrowedbooks():
    return jsonify([]) 

####################################################################################

def addbook_db(booktitle, bookisbn, imgfilename):
    # TODO: test
    with engine.connect() as con:
        data = ( { "isbn": bookisbn, "title": booktitle, "img_filname": imgfilename } )
        con.execute(text("""INSERT INTO books (isbn, title, img_filname) 
            VALUES(:isbn, :title, :img_filname)"""), data)

def list_books_db():
    # for addbooks
    # TODO: test
    with engine.connect() as con:
        res = con.execute("select isbn, title, img_filname from books").fetchall()
        ret = []
        for i in res:
            ret.append({ "isbn": i['isbn'], "title": i['title'], "filename":i['img_filname'] })
        return ret

def list_users_db():
    # TODO
    # test
    with engine.connect() as con:
        ret = []
        res = con.execute(
                """ SELECT users.username, books.title, booksinuse.borrow_date
                    FROM booksinuse 
                    INNER JOIN users ON users.id = booksinuse.user_id
                    INNER JOIN books ON books.id = booksinuse.book_id """).fetchall()
        for i in res:
            #print(i)
            ret.append({ "username": i['username'], "title":i['title'], "borrow_date": i['borrow_date'] })

        res = con.execute(
                """ SELECT username 
                    FROM users 
                    WHERE username 
                    NOT IN (
                        SELECT users.username
                        FROM booksinuse 
                        INNER JOIN users ON users.id = booksinuse.user_id
                        INNER JOIN books ON books.id = booksinuse.book_id
                    ) AND user_role != 0; """).fetchall()
        for i in res:
            #print(i)
            ret.append({ "username": i['username']})
        print(ret)
        return ret

def list_borrowed_books_db(username):
    # for user home page
    # TODO: 
    # test
    with engine.connect() as con:
        data = ( { "username": username } )
        res = con.execute(text(
                """ SELECT  books.title, booksinuse.borrow_date
                    FROM booksinuse 
                    INNER JOIN users ON users.id = booksinuse.user_id
                    INNER JOIN books ON books.id = booksinuse.book_id
                    where username = (:username) """), data).fetchall()
        ret = []
        for i in res:
            #print(i)
            ret.append({ "title":i['title'], "borrow_date": i['borrow_date'] })
        return ret

def list_book_by_title_db(booktitle):
    # for user home page
    # TODO: 
    # list only available books
    # smart search 
    with engine.connect() as con:
        data = ( { "title": booktitle } )
        res = con.execute(text(
                """ SELECT title, isbn FROM books WHERE title = (:title) """), data).fetchall()
        ret = []
        for i in res:
            #print(i)
            ret.append({ "title":i['title'], "isbn": i['isbn'] })
        return ret

def list_book_by_isbn_db(isbn):
    # for user home page
    # TODO: 
    # list only available books
    with engine.connect() as con:
        data = ( { "isbn": isbn } )
        res = con.execute(text(
                """ SELECT title, isbn FROM books WHERE isbn = (:isbn) """), data).fetchall()
        ret = []
        for i in res:
            #print(i)
            ret.append({ "title":i['title'], "isbn": i['isbn'] })
        return ret