from flask import Flask, session, render_template, redirect, Blueprint, request
from utils.query import query
from utils.errorResponse import errorResponse
import time

ub = Blueprint('user', __name__, url_prefix = '/user', template_folder='templates')

@ub.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        def filter_fn(user):
            return request.form['username'] in user and request.form['password'] in user
        user = query('SELECT * FROM user', [], 'select')
        login_success = list(filter(filter_fn, user))
        if not len(login_success):
            return errorResponse('Invalid username or password!')
        session['username'] = request.form['username']
        return redirect('/page/home')

@ub.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form['username']
        password = request.form['password']
        check_password = request.form['checkPassword']

        if password != check_password:
            return errorResponse('Passwords do not match!')

        def filter_fn(user):
            return username == user[0]

        users = query('SELECT username FROM user', [], 'select')

        print("Existing users:", users)

        filter_list = list(filter(filter_fn, users))
        if len(filter_list):
            print("Username already exists.")
            return errorResponse('Username is already registered!')
        else:
            time_tuple = time.localtime(time.time())
            create_time = f"{time_tuple[0]}-{time_tuple[1]:02d}-{time_tuple[2]:02d}"
            print("Creating user:", username, password, create_time)
            query('INSERT INTO user (username, password, createTime) VALUES (%s, %s, %s)',
                  [username, password, create_time])
            return redirect('/user/login')

@ub.route('/logOut',methods=['GET','POST'])
def logOut():
    session.clear()
    return redirect('/user/login')