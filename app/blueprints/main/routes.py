from flask import render_template, abort, flash
from flask_login import login_required, current_user

from . import bp as main
from .models import Product, Cart
from app import store, back

@main.route('/')
def index():
	products = Product.query.all()
	store('main.index')
	return render_template('index.html', products=products)

@main.route('/go_back/<int:amt>')
def go_back(amt):
	return back(amt)

@main.route('/product/<int:id>')
def product(id):
	product = Product.query.get(id)
	if not product:
		abort(404)
	store('main.product', {'id': id})
	return render_template('product.html', product=product, main_view=True)

@main.route('/add_to_card/<int:id>')
@login_required
def add_to_cart(id):
	product = Product.query.get(id)
	if not product:
		abort(404)
	item = Cart(current_user.id, product.id)
	item.save()
	flash(f"{product.name} added to cart", 'success')
	return back()

@main.route('/cart')
@login_required
def cart():
	carts = Cart.query.filter_by(user_id=current_user.id).all()
	products = [cart.product for cart in carts]
	total = 0
	for i in range(len(products)):
		products[i].cart_id = carts[i].id
		total += products[i].price
	store('main.cart')
	return render_template('index.html', products=products, total=total, cart_view=True)

@main.route('/remove_from_cart/<int:id>')
@login_required
def remove_from_cart(id):
	cart = Cart.query.get(id)
	if not cart:
		abort(404)
	if cart.user_id != current_user.id:
		abort(403)
	cart.delete()
	return back()

@main.route('/empty_cart')
@login_required
def empty_cart():
	carts = Cart.query.filter_by(user_id=current_user.id).all()
	#You DID say to do it one at a time in the instructions...
	for cart in carts:
		cart.delete()
	return back()