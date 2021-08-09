from app import db

class Product(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	description = db.Column(db.Text)
	#Price is in cents, prevents rounding errors
	price = db.Column(db.Integer)
	image = db.Column(db.String)
	carts = db.relationship('Cart', backref='product', lazy='dynamic')

	def __str__(self):
		return f"${self.price / 100} <{self.name}: {self.description} ({self.id})>"

class Cart(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
	product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

	def __init__(self, user_id, product_id):
		self.user_id = user_id
		self.product_id = product_id

	def save(self):
		db.session.add(self)
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()