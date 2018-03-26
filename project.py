from flask import Flask, render_template, url_for

project = Flask(__name__)

'''if __name__= "__main__":
    andela.run() '''

#home page
@project.route('/')
def home():
    return render_template('home.html') 

#layout
@project.route('/layout')
def layout():
    return render_template('layout.html')        



