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
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'such secret'    
#app.config['UPLOAD_FOLDER'] = './uploads'

engine = create_engine('postgresql+psycopg2://mrk1:qazwsxedc@localhost/yazlab3')

# TODO: 
# backend over do tests
# do flash error, warnings
# experiment whit improc

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/admin')
# admin root
def admin_root():
    # TODO:
    # print time
    now = datetime.datetime.now().strftime("%Y-%m-%d")
    print(now)
    return render_template('admin.html', now = now)

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
            return redirect(url_for('admin_root'))
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
def add_book():
    # TODO:
    # pass info about upload status

    if request.method == 'POST':
        f = request.files['file']
        f_extension = f.filename.split(".")[-1]
        f.filename = uuid1().__str__() + "." + f_extension
        f.save('./uploads/' + secure_filename(f.filename))
        isbn = readisbn(f.filename)
        booktitle = request.form['title']        
        if isbn is None:
            # pass info about upload status
            flash('cant detect isbn')
            return render_template('addbook.html', books = list_books_db())
        else:
            # pass info about upload status
            addbook_db(booktitle,isbn,f.filename)
            flash('book added')
            return render_template('addbook.html', books = list_books_db())

    return render_template('addbook.html', books = list_books_db())

@app.route('/admin/forwardtime')
def forward_time():
    # TODO: 
    # chage system time
    now = datetime.datetime.now()
    new_date = now + datetime.timedelta(days=20)
    command_string = "sudo date +%Y-%m-%d -s " + new_date.strftime("%Y-%m-%d")
    os.system(command_string)
    print(url_for('admin_root'))
    return redirect(url_for('admin_root'))
 
@app.route('/admin/listuser')
# list borrowed books also
def list_user():
    now = datetime.datetime.now().strftime("%Y-%m-%d")
    return render_template('listuser.html', users = list_users_db())

@app.route('/user')
# user root
def user_root():
    # TODO:
    # check user logged
    # print time
    borrowed_books = list_borrowed_books_db(session['username'])
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
def query_book():
    # search for all books
    if request.method == 'POST':
        if len(request.form['isbn']) == 0  and isinstance(request.form['title'], str):
            return render_template('querybook.html', books = list_book_by_title_db(request.form['title']))
        elif len(request.form['title']) == 0  and isinstance(request.form['isbn'], str):
            return render_template('querybook.html', books = list_book_by_isbn_db(request.form['isbn']))
        else:
            flash("use only title or isbn")
            render_template('querybook.html')

    # list only available books
    books = list_available_books_db()
    return render_template('querybook.html', books = books)

# if have time refactor other evaluations to this
# logic can be improved
# control flow can be improved to prevent code duplication
@app.route('/user/borrowbook', methods=('GET', 'POST'))
def borrow_book():
    borrowed_books = list_borrowed_books_db(session['username'])
    available_books = list_available_books_db()
    if request.method == "POST":
        username = session['username']
        isbn = request.form['isbn']
        title = request.form['title']

        if len(isbn) > 0 and len(title) > 0:
            flash("use only title or isbn")
        elif len(isbn) > 0  or len(title) > 0:
            
            if check_user_permitted(username) == False:
                return render_template('borrowbook.html', borrowed_books = borrowed_books, available_books= available_books)

            if check_book_available(title, isbn) == False:
                return render_template('borrowbook.html', borrowed_books = borrowed_books, available_books= available_books)

            # give book to user !
            if len(isbn) > 0:
                book_id = get_book_id_by_isbn_db(isbn)
            else:
                book_id = get_book_id_by_title_db(title)
            
            # now = get_now_db() backup option
            # get datetime + 7 day
            now = datetime.datetime.now()
            return_date = now + datetime.timedelta(days=7)
            user_id = session['user_id']
            print("user_id: ", user_id)
            print("now: ", now)
            print("return_date: ", return_date)
            # TODO: 
            # test control flow and crud
            # check output no best practice for control flow
            give_book_to_user_db(book_id,return_date,user_id)
            #print('succes')
            flash('succes')
            
            borrowed_books = list_borrowed_books_db(session['username'])
            available_books = list_available_books_db()
            render_template('borrowbook.html', borrowed_books = borrowed_books, available_books= available_books)
            #return redirect(url_for('borrow_book'))

        elif len(isbn) == 0  and len(title) == 0:
            flash('empty form')

    return render_template('borrowbook.html', borrowed_books = borrowed_books, available_books= available_books)  

def check_user_permitted(username):
    # check user book count
    c = get_borrowed_count_db(username)
    if c >= 3:
        print('no limit')
        flash('no limit') 
        return False
    print('have limit')

    # check user have overdue book
    c = check_overdued_book_db(username)
    if c:
        print('no overdued book')
        return True
    else:
        print('have overdued book!')
        flash('have overdued book')
        return False

def check_book_available(title, isbn):
    available_books = list_available_books_db()
    print(available_books)
    for book in available_books:
        # print(book['isbn'],type(book['isbn']))
        if book['title'] == title:
            print('book available: ', title)
            return True
        if book['isbn'] == isbn:
            print('book available: ', isbn)
            return True
    
    flash_str = 'cant find book: ' + title + "," + isbn + " or in use"
    flash(flash_str)
    print(flash_str)
    return False

@app.route('/user/returnbook', methods=('GET', 'POST'))
# TODO: 
# upload img
def return_book():
    borrowed_books = list_borrowed_books_db(session['username'])
    if request.method == "POST":
        username = session['username']
        
        f = request.files['file'] # werkzeug filestorage
        f_extension = f.filename.split(".")[-1]
        f.filename = uuid1().__str__() + "." + f_extension
        f.save('./uploads/' + secure_filename(f.filename))
        img_isbn = readisbn(f.filename)    
        
        if img_isbn is None:
            print('cant detect isbn')
            flash('cant detect isbn')
            return redirect(url_for('return_book'))
        else:
            # check user borrowed that book 
            print(img_isbn)
            for book in borrowed_books:
                if book['isbn'] == img_isbn:
                    # return book db
                    print('book returned')
                    flash('book returned')
                    return_book_db(img_isbn)
                    return redirect(url_for('return_book'))
            flash('isbn dont match with borrwed books isbn')
            print('isbn dont match with borrwed books isbn')

        return redirect(url_for('return_book'))

    return render_template('returnbook.html', borrowed_books = borrowed_books)

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
                """ SELECT users.username, books.title, booksinuse.return_date
                    FROM booksinuse 
                    INNER JOIN users ON users.id = booksinuse.user_id
                    INNER JOIN books ON books.id = booksinuse.book_id """).fetchall()
        for i in res:
            ret.append({ "username": i['username'], "title":i['title'], "return_date": i['return_date'] })

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
            ret.append({ "username": i['username']})
        return ret

def list_borrowed_books_db(username):
    # for user home page
    # TODO: 
    # test
    with engine.connect() as con:
        data = ( { "username": username } )
        res = con.execute(text(
                """ SELECT  books.title, books.isbn, booksinuse.return_date
                    FROM booksinuse 
                    INNER JOIN users ON users.id = booksinuse.user_id
                    INNER JOIN books ON books.id = booksinuse.book_id
                    where username = (:username) """), data).fetchall()
        ret = []
        for i in res:
            ret.append({ "title":i['title'], "return_date": i['return_date'], "isbn": i['isbn'] })
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
            ret.append({ "title":i['title'], "isbn": i['isbn'] })
        return ret

def list_available_books_db():
    # for user query
    # TODO: test
    with engine.connect() as con:
        res = con.execute(
            """SELECT title, isbn
                FROM books
                WHERE isbn
                NOT IN (
                    SELECT books.isbn
                    FROM books 
                    INNER JOIN booksinuse ON books.id = booksinuse.book_id)
            """).fetchall()
        ret = []
        for i in res:
            ret.append({ "title": i['title'], "isbn": i['isbn']})
        return ret

def get_borrowed_count_db(username):
    # TODO: test
    # better way to use res
    with engine.connect() as con:
        data = ( { "username": username } )
        res = con.execute(text(
            """ SELECT COUNT(u.username)
                FROM users u
                INNER JOIN booksinuse biu ON u.id = biu.user_id
                WHERE u.username = :username 
            """), data).fetchall()
        for i in res:
            return i['count']

def get_book_id_by_title_db(title):
    # TODO: test
    with engine.connect() as con:
        data = ( { "title": title } )
        res = con.execute(text(
            """ SELECT id FROM books WHERE title = :title """), data).fetchall()
        for i in res:
            #print(i['id'])
            return i['id']

def get_book_id_by_isbn_db(isbn):
    # TODO: test
    with engine.connect() as con:
        data = ( { "isbn": isbn } )
        res = con.execute(text(
            """ SELECT id FROM books WHERE isbn = :isbn """), data).fetchall()
        for i in res:
            #print(i['id'])
            return i['id']

def check_overdued_book_db(username):
    # TODO: test
    with engine.connect() as con:
        data = ( { "username": username } )
        dates = []
        res = con.execute(text(
            """ 
            SELECT biu.return_date
            FROM users u
            INNER JOIN booksinuse biu ON u.id = biu.user_id
            WHERE u.username = :username
            """), data).fetchall()
        for i in res:
            dates.append(i['return_date'])
        
        now = None
        #res = con.execute('SELECT NOW();')
        #for i in res:
        #    now = i['now']
        now = datetime.datetime.now()
        # kinda works 
        print('now: ', now)
        for date in dates:
            print('return date: ', date)
            if now > date:
                return False
        return True

def give_book_to_user_db(book_id, return_date, user_id):
    with engine.connect() as con:
        data = ( { "book_id": book_id, "return_date": return_date, "user_id": user_id } )
        con.execute(text("""INSERT INTO booksinuse (book_id, return_date, user_id) 
            VALUES(:book_id, :return_date, :user_id)"""), data)

def return_book_db(isbn):
    # TODO: 
    # test
    book_id = get_book_id_by_isbn_db(isbn)
    #print(book_id)
    
    with engine.connect() as con:
        data = ({ "book_id": book_id })
        con.execute(text("""DELETE FROM booksinuse WHERE book_id = :book_id"""), data)
    pass

def addbook_db(booktitle, bookisbn, imgfilename):
    # TODO: test
    with engine.connect() as con:
        data = ( { "isbn": bookisbn, "title": booktitle, "img_filname": imgfilename } )
        con.execute(text("""INSERT INTO books (isbn, title, img_filname) 
            VALUES(:isbn, :title, :img_filname)"""), data)

# returns datetime 
# not used
def get_now_db():
    with engine.connect() as con:
        res = con.execute("SELECT NOW()").fetchone()
        return res