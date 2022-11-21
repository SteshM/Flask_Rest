from flask import Flask, request, jsonify
from flask import json
from werkzeug.exceptions import HTTPException
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import logging
# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path. join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init na
ma = Marshmallow(app)

   # Product Class/Model
class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(100), unique=True)
  description = db.Column(db.String(200))
  price = db.Column(db.Float)
  qty = db.Column(db.Integer)
  
  def __init__(self,name,description,price,qty):
     self.name = name
     self.description = description
     self.price = price
     self.qty = qty
   
     #product schema
class ProductSchema(ma.Schema):
   class Meta:
      fields = ('id', 'name', 'description', 'price','qty')

      #init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

     #Create a Product
@app.route('/product',methods=['POST'] ) #This is a decorator that exposes endpoint which is a post
def add_product():
   app.logger.info("This method is used to POST")
   name = request.json['name']
   app.logger.info("about to add a product with name %s", name)
   description = request.json['description']
   app.logger.info("about to add a product with description %s", description)
   price = request.json['price']#price is a variable, we are assigning it the value of the parameter price. in our json request.
   app.logger.info("about to add a product with price %s", price)
   qty = request.json['qty']
   app.logger.info("about to add a product with qty %s", qty)
   new_product = Product(name, description,price,qty)#new_product is a variable of type product

   db.session.add(new_product)#insert record in the db
   db.session.commit()#commits the record 

   return product_schema.jsonify(new_product)# return json response

     #Get all products
@app.route('/product', methods=['GET'])
def get_products():
   app.logger.info("The method used is GET", request.method)

   all_products = Product.query.all()#all_products is a collection of products(list,arraylist)
   result = products_schema.dump(all_products)

   return jsonify(result)

   #Get a single product
@app.route('/product/<id>', methods=['GET'])#id is a path variable
def get_product(id):
   product = Product.query.get(id)
   return product_schema.jsonify(product)

   #update a product
@app.route ('/product/<id>', methods=['PUT'])
def update_product(id):
   product = Product.query.get(id)
   name = request.json['name']
   description = request.json['description']
   price = request.json['price']
   qty = request.json['qty']

   product.name = name
   product.description = description
   product.price = price
   product.qty = qty

   db.session.commit()
   
   return product_schema.jsonify(product)

   #delete Product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
      product = Product.query.get(id)
      db.session.delete(product)
      db.session.commit()

      return product_schema.jsonify(product)

   #total product Cost
@app.route('/product/price/<id>', methods=['GET'])#id is a path variable
def get_product_price(id):
   product = Product.query.get(id)
   name = product.name
   app.logger.info("retrieved product name %s",name) 
   desc = product.description
   price = product.price
   qty = product.qty
   total_price = qty * price
   app.logger.info("This is the total price : %s",total_price)
   data = {
            "name" : name ,
            "description":desc,
            "totalPrice": total_price
        }#created a dictionary and we are jsonifying it
  
   return jsonify(data)


      #Error handler
@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

 # Run Server
if __name__== '_main_':
  app.run(debug=True)






