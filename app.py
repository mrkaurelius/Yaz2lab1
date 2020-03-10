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

app = Flask(__name__)
app.config['SECRET_KEY'] = 'such secret'    
#app.config['UPLOAD_FOLDER'] = './uploads'

engine = create_engine('postgresql+psycopg2://mrk0:qazwsxedc@localhost/yazlab3')

# TODO: 
# build basic mechanism for auth
# fix admin user login
@app.route('/')
def home():
    # if user logged in redirect /user
    # if admin logged in redirect /admin
    # dont need non-auth home
    return render_template('home.html')

@app.route('/admin')
# admin root
def admin_root():
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
# book image required
# TODO: check admin
# implement different methods
def add_book():
    if request.method == 'POST':
        f = request.files['file']
        f_extension = f.filename.split(".")[-1]
        f.filename = uuid1().__str__() + "." + f_extension
        f.save('./uploads/' + secure_filename(f.filename))
        
        isbn = readisbn(f.filename)
        if isbn is None:
            # pass info about upload status
            return render_template('addbook.html')
        else:
            # add book entr to database
            # pass info about upload status
            return render_template('addbook.html')

    return render_template('addbook.html')

@app.route('/admin/forwardtime')
def forward_time():
    # no need html
    return redirect(url_for('admin_root'))
 
@app.route('/admin/listuser')
# list borrowed books also
def list_user():
    return 'listuser'

@app.route('/user')
# user root
def user_root():
    # user login ?
    # TODO: check user logged
    return render_template('user.html',username = session['username'])

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

@app.route('/user/querybook')
def query_book():
    return 'querybook'

@app.route('/user/borrowbook')
def borrow_book():
    return 'borrowbook'  

@app.route('/user/returnbook')
def return_book():
    return 'returnbook'  

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

@app.route('/json/db')
def db_dummy():
    # username password check
    ret = []
    with engine.connect() as con:
        rows = con.execute("select * from users")
        for row in rows:
            ret.append(dict(row))
    return jsonify(ret) 