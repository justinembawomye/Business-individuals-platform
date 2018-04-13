from flask import Flask, render_template, url_for, flash, request, logging, session, redirect
from wtforms import StringField, PasswordField, TextAreaField, Form, validators
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from functools import wraps



#businesses = ['cakeven', 'yummy', 'S&D center', 'klassy kids store', 'K2 supermarket', 'kiest', 'volttech.co','nummies', 'upright inv']

project= Flask(__name__)



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
    return render_template('home.html') 

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



def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap    

#logout
@project.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')

    return redirect(url_for('home'))


'''@project.route('/dashboard')
@is_logged_in
def dashboard():
    return render_template('dashboard.html')'''



#dashboard
@project.route('/dashboard')
@is_logged_in
def dashboard():
    #create cursor
    cur = mysql.connection.cursor()

    #Get tasks
    result = cur.execute("SELECT * FROM business WHERE owner = %s",  [session['username']] )


    business = cur.fetchall()

    if result > 0:
        return render_template('dashboard.html', business=business)
    else:
        msg ="No tasks Found"    
        return render_template('dashboard.html', msg=msg)

     #close connection
    cur.close()   




@project.route('/search')
@is_logged_in
def search():
    #create cursor
    cur = mysql.connection.cursor()

    #Get tasks
    result = cur.execute("SELECT * FROM business WHERE catergory = %s",  [catergory])


    business = cur.fetchone()

    if result > 0:
        return render_template('search.html', business=business)
    else:
        msg ="Business not Found"    
        return redirect(url_for('home', msg=msg))

     #close connection
    cur.close()   






#Task Form class
#WTforms
class TaskForm(Form):
    business_name= StringField('Business_name',[validators.Length(min=1, max=150)])  
    description = TextAreaField('Description',[validators.Length(min=5)])
    
    

#Add_tasks
@project.route('/add_business', methods = ['GET', 'POST'])
@is_logged_in
def add_business():
   form = TaskForm(request.form)
   if request.method == 'POST' and form.validate():
       business_name = form.business_name.data
       description = form.description.data


       #create cursor
       cur = mysql.connection.cursor()


      #Execute
       cur.execute("INSERT  INTO business(business_name, description, owner) VALUES(%s, %s, %s)",  (business_name, description, session['username']))

      #commit
       mysql.connection.commit()
      

      #close connection
       cur.close()
 
      #flash
       flash('business added',  'success')

       return redirect(url_for('dashboard'))

   return render_template('add_business.html',  form=form) 
                     


#edit_tasks
@project.route('/edit_business/<string:id>', methods = ['GET', 'POST'])
@is_logged_in
def edit_tasks(id):

    #Create cursor
    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM business WHERE id = %s", [id]) 

    business = cur.fetchone()

   #Get form
    form = TaskForm(request.form)

   #Populate the forms
    form.business_name.data = business['business_name']
    form.description.data = business['description']


    if request.method == 'POST' and form.validate():
       business_name = request.form['business_name']
       body = request.form['description']


       #create cursor
       cur = mysql.connection.cursor()


      #Execute
       cur.execute("UPDATE business SET business_name = %s, description = %s WHERE id = %s", (business_name, description, id))
      #commit
       mysql.connection.commit()
      

      #close connection
       cur.close()
 
      #flash
       flash('Business updated', 'success')

       return redirect(url_for('dashboard'))

    return render_template('edit_business.html',  form=form) 




    #Delete task
@project.route('/delete_business/<string:id>', methods =['POST'])
@is_logged_in
def delete_business(id):
    #create cursor
    cur = mysql.connection.cursor()

    #execute
    cur.execute("DELETE FROM business WHERE id = %s", [id])

    #commit DB
    mysql.connection.commit()

    #close cursor
    cur.close()

    flash('Business deleted', 'success')

    return redirect(url_for('dashboard'))

                     






    
