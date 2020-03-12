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
# do flash error, warnings
# dont expire sessions 

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/admin')
# admin root
def admin_root():
    # TODO:
    # print time
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
def add_book():
    # TODO: check if user admin (no need)
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
    # TODO: 
    # chage system time
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
# TODO:
# list all books
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
@app.route('/user/borrowbook', methods=('GET', 'POST'))
# TODO:
# check user permitted
# check book available
# print errors use flash
def borrow_book():
    borrowed_books = list_borrowed_books_db(session['username'])
    if request.method == "POST":
        username = session['username']
        isbn = request.form['isbn']
        title = request.form['title']

        # search by title
        if len(isbn) == 0  and len(title) > 0:
            if check_user_permitted(username) == False:
                return render_template('borrowbook.html', borrowed_books = borrowed_books)

            if check_book_available(title) == False:
                return render_template('borrowbook.html', borrowed_books = borrowed_books)

            # give book to user !
            print('succes')
            flash('succes')
            borrowed_books = list_borrowed_books_db(session['username'])
            render_template('borrowbook.html', borrowed_books = borrowed_books)

        # search by isbn
        elif len(title) == 0  and len(isbn) > 0:
            # not impelemented
            return redirect(url_for('borrow_book'))

        else:
            flash("use only title or isbn")
        

    return render_template('borrowbook.html', borrowed_books = borrowed_books)  


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

def check_book_available(title):
    # BURADA KALDIM
    available_books = list_available_books_db()
    print(available_books)
    for book in available_books:
        #print(book,type(book),book['title'], book['isbn'])
        if book['title'] == title:
            print('book available: ', title)
            return True
    flash_str = 'cat find book: ' + title
    flash(flash_str)
    print(flash_str)
    return False

@app.route('/user/returnbook')
def return_book():
    # TODO:
    # upload img
    # build mechanism for user input
    return 'returnbook'  

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
                """ SELECT  books.title, booksinuse.return_date
                    FROM booksinuse 
                    INNER JOIN users ON users.id = booksinuse.user_id
                    INNER JOIN books ON books.id = booksinuse.book_id
                    where username = (:username) """), data).fetchall()
        ret = []
        for i in res:
            ret.append({ "title":i['title'], "return_date": i['return_date'] })
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