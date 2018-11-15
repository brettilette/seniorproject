from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)
@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html', title = 'Home')
@app.route('/createProject', methods=['GET','POST'])
def createProjectPage():
    return render_template('createProject.html', title = 'Create Project')
@app.route('/editProject')
def editProjectPage():
    return render_template('editProject.html', title = 'Edit Project')
@app.route('/viewProject')
def viewProjectPage():
    return render_template('viewProject.html', title = 'View Project')
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', title = 'Dashboard')
