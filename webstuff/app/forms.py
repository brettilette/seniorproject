from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Optional
from app.models import User

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('This username is taken')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('This Email is already registered')

class CreateProjectForm(FlaskForm):
	company = StringField('Target Company', validators=[DataRequired()])
	submit = SubmitField('Submit')

class EditProjectForm(FlaskForm):
	email = StringField('Email Account', validators=[Email(), Optional()])
	twitter = StringField('Twiter Handle', validators=[Optional()])
	submit = SubmitField('Submit')

class SelectProjectForm(FlaskForm):
	project = SelectField('Project', choices=[])
	submit = SubmitField('Submit')