from flask import Flask, render_template, url_for, flash, request, logging, session, redirect
from wtforms import StringField, PasswordField, TextAreaField, Form, validators
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt



businesses = ['cakeven', 'yummy', 'S&D center', 'klassy kids store', 'K2 supermarket', 'kiest', 'volttech.co','nummies', 'upright inv']

project= Flask(__name__)

if__name__="__main__":

'''if __name__= "__main__":
    project.run() '''
project.secret_key='justine123'

project.config['MYSQL_HOST'] = 'localhost'
project.config['MYSQL_USER'] = 'root'
project.config['MYSQL_PASSWORD'] = 'justine'
project.config['MYSQL_DB'] = 'businessproject'
project.config['MYSQL_CURSORCLASS']= 'DictCursor'

mysql = MySQL(project)   

#home page
@project.route('/')
def home():
    return render_template('home.html', task=task) 

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


    

#user_register
@project.route('/user_register', methods=['POST', 'GET'])
def user_register():
    form = Account(request.form)

    if request.method == 'POST'and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))



        cur = mysql.connection.cursor()


        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))
       
       
        mysql.connection.commit()

        cur.close()

        flash('You are now registered and can login', 'success')

        return redirect(url_for('login'))

    return render_template('user_register.html', form=form)


#user login
@project.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']
         #create cursor

        cur = mysql.connection.cursor()

        #get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username]) 

        if result > 0:
            data = cur.fetchone()
            password = data['password']


        #compare passwords
        if sha256_crypt.verify(password_candidate, password):
            project.logger.info('Password matched') 

            session['logged_in'] = True
            session['username'] = username

            flash('You are logged in', 'success')

            return redirect(url_for('dashboard'))

            #close connection
            cur.close()


        else:
             error = "Invalid login"
             return render_template('login.html', error=error)  
    else:
        error = "Username not found"
        return render_template('login.html', error=error)       

            

    return render_template('login.html')       


#logout
@project.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')

    return redirect(url_for('home'))


@project.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')





    
