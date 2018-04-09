from flask import Flask, render_template, url_for, flash, request, logging, session, redirect
from wtforms import StringField, PasswordField, TextAreaField, Form, validators
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt



businesses = ['cakeven', 'yummy', 'S&D center', 'klassy kids store', 'K2 supermarket', 'kiest', 'volttech.co','nummies', 'upright inv']

project= Flask(__name__)

'''if __name__= "__main__":
    project.run() '''


project.config['MYSQL_HOST'] = 'localhost'
project.config['MYSQL_USER'] = 'root'
project.config['MYSQL_PASSWORD'] = 'justine'
project.config['MYSQL_DB'] = 'businessproject'
project.config['MYSQL_CURSORCLASS']= 'DictCursor'

mysql = MySQL(project)   

#home page
@project.route('/')
def home():
    return render_template('home.html', businesses=businesses) 

#layout
@project.route('/layout')
def layout():
    return render_template('layout.html')   


#create_account form class
class Account(Form):
    name = StringField('Name', [validators.Length(min=4, max=50)])
    email = StringField('Email', [validators.Length(min=6, max=100)])
    username = StringField('Username', [validators.Length(min=4, max=30)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message= 'Passwords do not match')
    ])
    confirm = PasswordField('confirm password')


#create account
@project.route('/create_account', methods = ['GET', 'POST'])
def create_account():
    form = Account(request.form)
    if request.method == 'POST' and form.validate():
        '''name = form.name.data()
        username = form.username.data
        email= form.email.data
        password = sha256_crypt.encrypt(str('password'))'''
        return render_template('create_account.html')
        
         
    return render_template('create_account.html', form=form)      




'''@project.route('/account', methods=["GET", "POST"])
def registerr():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        passwordd = request.form.get('passwordd')

        #create cursor
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))
        
        #commit to db
        mysql.connection.commit()

        #close connection
        cur.close()
        
        return redirect(url_for('home'))
    else:
        return render_template("account.html")'''       

@project.route('/login', methods = ['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']
    return render_template('login.html')
    

