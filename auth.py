########################################################################################
######################          Import packages      ###################################
########################################################################################
# from Tracker.Tracker.models import Expense
# from Tracker.Tracker.models import Expense
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import *
from flask_login import login_user, logout_user, login_required, current_user
from __init__ import db
from datetime import datetime
from sqlalchemy import text

auth = Blueprint('auth', __name__) # create a Blueprint object that we name 'auth'

@auth.route('/DummyTable', methods=['GET', 'POST'])
def DummyTable():
    if request.method == "GET":
        return render_template('DummyTable.html')
    else:
        cat = request.form.get('cat')
        acc = request.form.get('acc')
        purpose = request.form.get('purpose')
        exp = request.form.get('exp')
        # dt= request.form.get('date')
        id = request.form.get('id')
        uid = current_user.get_id()
        desc="Bank Transaction"
        dt=datetime.now()
        print(type(dt))
        new_DummyTable = dummy_table(Transaction_Id = id, Account_No = acc, Category = cat, Purpose = purpose, Expense = exp,Date=datetime.now())
        db.session.add(new_DummyTable)
        
        new_data = Expense(userid = uid, category = cat, desc = desc, expense = exp,datetime=datetime.now())
        db.session.add(new_data)
        
        db.session.commit()
        return redirect(url_for('main.data'))
        
@auth.route('/login', methods=['GET', 'POST']) # define login page path
def login(): # define login page fucntion
    if request.method=='GET': # if the request is a GET we return the login page
        return render_template('login.html')
    else: # if the request is POST the we check if the user exist and with te right password
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        user = User.query.filter_by(email=email).first()
        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user:
            flash('Please sign up before!')
            return redirect(url_for('auth.signup'))
        elif not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page
        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=remember)
        return redirect(url_for('main.profile'))

@auth.route('/signup', methods=['GET', 'POST'])# we define the sign up path
def signup(): # define the sign up function
    if request.method=='GET': # If the request is GET we return the sign up page and forms
        return render_template('signup.html')
    else: # if the request is POST, then we check if the email doesn't already exist and then we save data
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
        if user: # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))
        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256')) #
        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))

@auth.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == "GET":
        return render_template('profile.html')
    else:
        cat = request.form.get('cat')
        desc = request.form.get('desc')
        exp = request.form.get('exp')
        # dt= request.form.get('date')
        id = current_user.get_id()
        dt=datetime.now()
        print(type(dt))
        new_data = Expense(userid = id, category = cat, desc = desc, expense = exp,datetime=datetime.now())
        db.session.add(new_data)
        #sql = text(''' INSERT INTO Expense (category, desc, expense, datetime) SELECT Category, Purpose, Expense, Date FROM dummy_table ''')
        #db.session.execute(sql)
        db.session.commit()
        return redirect(url_for('main.data'))



@auth.route('/logout') # define logout path
@login_required
def logout(): #define the logout function
    logout_user()
    return redirect(url_for('main.index'))
    #        Expense.query.filter_by(INSERT INTO Expense [(category, desc, expense, datetime)] SELECT [(Category, Purpose, Expense, Date)] FROM dummy_table).all()
    #("INSERT INTO Expense [(category, desc, expense, datetime)] SELECT [(Category, Purpose, Expense, Date)] FROM dummy_table" ),(cat, desc, exp, dt)
    
