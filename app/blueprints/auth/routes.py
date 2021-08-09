from flask_login import login_user, logout_user, current_user, login_required
from flask import render_template, request, redirect, url_for, flash

from .models import User
from . import bp as auth
from .forms import RegisterForm, LoginForm
from app import back

@auth.route('/logout')
@login_required
def logout():
	if current_user:
		flash('Logged out', 'warning')
		logout_user()
	return back()

@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if request.method == 'POST' and form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user and user.check_hashed_password(form.password.data):
			login_user(user)
			flash('Logged in', 'success')
			return back()
		else:
			flash('Invalid credentials', 'danger')
			return redirect(url_for('auth.login'))
	return render_template('login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm()
	if request.method == 'POST' and form.validate_on_submit():
		try:
			data = {
				'username': form.username.data,
				'password': form.password.data
			}
			user = User()
			user.from_dict(data)
			flash('Registered', 'success')
			return redirect(url_for('auth.login'))
		except:
			flash('Error', 'danger')
	return render_template('register.html', form=form)