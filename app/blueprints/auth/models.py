from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String, index=True, unique=True)
	password = db.Column(db.String)

	def from_dict(self, data):
		self.username = data['username']
		self.password = self.hash_password(data['password'])
		self.save()

	def __str__(self):
		return f"<{self.username} ({self.id})>"

	def hash_password(self, original_password):
		return generate_password_hash(original_password)

	def check_hashed_password(self, login_password):
		return check_password_hash(self.password, login_password)

	def save(self):
		db.session.add(self)
		db.session.commit()

@login.user_loader
def load_user(id):
	return User.query.get(int(id))