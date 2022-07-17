########################################################################################
######################    Developed by TinaD11       ###################################
########################################################################################
########################################################################################
######################          Import packages      ###################################
########################################################################################
from flask import Blueprint, render_template, request,flash
from flask_login import login_required, current_user
from __init__ import create_app, db
from models import *

########################################################################################
# our main blueprint
main = Blueprint('main', __name__)

@main.route('/DummyTable') # DummyTable page that return 'DummyTable'
def DummyTable():
    return render_template('DummyTable.html') 

@main.route('/about') # about us page that return 'about us'
def about():
    return render_template('about.html')
@main.route('/contact') # contact page that return 'contact'
def contact():
    return render_template('contact.html')    
    
@main.route('/') # home page that return 'index'
def index():
    return render_template('index.html')

    
    

@main.route('/profile') # profile page that return 'profile'
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)
@main.route('/data') # profile page that return 'profile'
@login_required
def data():
    userid = current_user.get_id()
    full_data = Expense.query.filter_by(userid=userid)
    return render_template('data.html',data=full_data,name=current_user.name)
    
@main.route('/datachart') 
@login_required
def datachart():
    userid = current_user.get_id()
    full_data = Expense.query.filter_by(userid=userid)
    #pie chart----------------
    t_g=0
    t_f=0
    t_c=0
    t_e=0
    t_fu=0
    t_h=0
    t_sal=0
    
        #-grocery
    gr = Expense.query.filter_by(category = "Grocery",userid=userid)
    for i in gr:
        t_g+=i.expense
        #-Food
    fd = Expense.query.filter_by(category = "Food",userid=userid)
    for i in fd:
        t_f+=i.expense
        #-Clothing
    cl = Expense.query.filter_by(category = "clothing",userid=userid)
    for i in cl:
        t_c+=i.expense
        #-Entertainment
    et = Expense.query.filter_by(category = "Entertainment",userid=userid)
    for i in et:
        t_e+=i.expense
        #Fuel
    fu = Expense.query.filter_by(category = "Fuel",userid=userid)
    for i in fu:
        t_fu+=i.expense
        #Health
    hlth = Expense.query.filter_by(category = "Health",userid=userid)
    for i in hlth:
        t_h+=i.expense
        #-Salary
    sal = Expense.query.filter_by(category = "Salary",userid=userid)
    for i in sal:
        t_sal+=i.expense
    savings =t_sal-(t_g+t_f+t_c+t_e+t_fu+t_h)
    #pie chart-end----------------
    print(t_g)
    return render_template('datachart.html',data=full_data,name=current_user.name,groc=t_g,food=t_f,cloth=t_c,entertainment=t_e,fuel=t_fu,health=t_h,salary=t_sal,saving=savings)

    
app = create_app() # we initialize our flask app using the __init__.py function
if __name__ == '__main__':
    db.create_all(app=create_app()) # create the SQLite database
    app.run(debug=True) # run the flask app on debug mode