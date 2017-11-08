from flask import request,jsonify,Blueprint
from my_app import app,db
from my_app.catalog.models import Product,Category

catalog = Blueprint('catalog',__name__)

@catalog.route('/')
@catalog.route('/home')
def home():
	return "welcome to the Catalog home"

@catalog.route('/products')
def products():
	products = Product.query.all()
	res = {}
	for product in products:
		res[product.id] = {
			'name' : product.name,
			'price' : product.price,
			'category': product.category.name
		}
	return jsonify(res)

@catalog.route('/product-create',methods = ['POST'])
def create_product():
	name = request.form .get('name')
	price = request.form.get('price')
	categ_name = request.query.filter_by(name = categ_name).first()
	if not category:
		category = Category(categ_name)
	product = Product(name, price, category)
	db.session.add(product)
	db.session.commit()
	return 'Product created'

@catalog.route('/category-create',methods = ['POST'])
def create_category():
	name = request.form.get('name')
	category = Category(name)
	db.session.add(category)
	db.session.commit()
	return 'Category created...'

@catalog.route('/categories')
def categories():
	categories = Category.query.all()
	res = {}
	for category in categories:
		res[category.id] = {
			'name' : category.name
		}
		res[category.id]['products'] = []
		for product in category.products:
			res[category.id]['products'].append(
				{
					'id' : product.id,
					'name' : product.name, 
					'price' : product.price
				}
				)

	return jsonify(res)
# @product_blueprint.context_processor
# def some_processor():
# 	def full_name(product):
# 		a = 5
# 		b = 6
# 		return (a+b)
# 	return {'full_name':full_name}

# @product_blueprint.template_filter('reverse')
# def reverse_filter(s):
# 	return s[::-1]

# @product_blueprint.template_filter('full_name')
# def full_name_filter(product):
# 	return '{1}/{0}'.format(product['category'],product['name'])
