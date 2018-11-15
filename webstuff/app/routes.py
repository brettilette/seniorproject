from flask import render_template
from app import app

@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html', title = 'Home')
@app.route('/createProject')
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
