from flask import Flask, session, url_for, redirect
from config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Login required for that page'
login.login_message_category = 'danger'
db = SQLAlchemy()
migrate = Migrate()

def store(name, vars = {}):
	if not session.get('stack'):
		session['stack'] = []
	#Flask will only keep changes to session keys if they're set directly, not if they're modified
	#This took me way too long to solve
	#Pain
	stack = session['stack'][:]
	stack.append([name, vars])
	session['stack'] = stack

def back(amt=1):
	stack = session.get('stack')
	if stack and len(stack) >= amt:
		page = stack[-amt]
		session['stack'] = stack[:len(stack) - amt]
		return redirect(url_for(page[0], **page[1]))
	return redirect(url_for('main.index'))

def create_app(config=Config):
	app = Flask(__name__)
	app.config.from_object(config)
	
	login.init_app(app)
	db.init_app(app)
	migrate.init_app(app, db)

	app.jinja_env.globals.update(back=back)

	from .blueprints.main import bp as mainbp
	app.register_blueprint(mainbp)

	from .blueprints.auth import bp as authbp
	app.register_blueprint(authbp)

	return app