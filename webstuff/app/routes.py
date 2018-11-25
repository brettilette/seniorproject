from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, CreateProjectForm, EditProjectForm, SelectProjectForm
from app.models import User


company = 'none'
companies = [('test1', 'test1'), ('test2', 'test2')]

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('home')
		return redirect(next_page)
	return render_template('login.html', title='Login', form=form)
@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))
@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('login'))
	return render_template('register.html', title="Registration", form=form)
@app.route('/')
@app.route('/home')
@login_required
def home():
	return render_template('home.html', title = 'Home', company=company)
@app.route('/createProject', methods=['GET','POST'])
def createProjectPage():
	form = CreateProjectForm()
	if form.validate_on_submit():
		#add create project function
		return redirect(url_for('home'))
	return render_template('createProject.html', title = 'Create Project', form=form)
@app.route('/editProject', methods=['GET', 'POST'])
def editProjectPage():
	form = EditProjectForm()
	#add edit project function
	return render_template('editProject.html', title = 'Edit Project', form=form)
@app.route('/dashboard')
def dashboard():
	iframe = 'https://www.google.com/'
	# set iframe to kibana dashboard 
	return render_template('dashboard.html', title = 'Dashboard', iframe=iframe)
@app.route('/selectProject', methods=['GET', 'POST'])
def selectProject():
	form = SelectProjectForm()
	form.project.choices = companies
	if request.method == 'POST':
		global company
		company = form.project.data
		return redirect(url_for('home'))
	return render_template('selectProject.html', title = 'Select Project', form=form)
