from werkzeug import abort
from flask import render_template
from flask import Blueprint
from my_app.product.models import PRODUCTS

product_blueprint = Blueprint('produ',__name__)

@product_blueprint.route('/')
@product_blueprint.route('/home')
def home():
	return render_template('home.html',products = PRODUCTS)

@product_blueprint.route('/product/<key>')
def product(key):
	product = PRODUCTS.get(key)
	print(product)
	if not product:
		abort(404)
	return render_template('product.html', product=product)

@product_blueprint.context_processor
def some_processor():
	def full_name(product):
		a = 5
		b = 6
		return (a+b)
	return {'full_name':full_name}

# @product_blueprint.template_filter('reverse')
# def reverse_filter(s):
# 	return s[::-1]

@product_blueprint.template_filter('full_name')
def full_name_filter(product):
	return '{1}/{0}'.format(product['category'],product['name'])

	