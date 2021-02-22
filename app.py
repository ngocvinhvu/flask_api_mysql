from os import name
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from db import db

from resources.user import UserRegister
from security import authenticate, identity
from resources.customer import Customer, CustomerList
from resources.employee import Employee, EmployeeList
from resources.office import Office, OfficeList
from resources.orderdetail import Orderdetail, OrderdetailList
from resources.order import Order, OrderList
from resources.payment import Payment, PaymentList
from resources.productline import Productline, ProductlineList
from resources.product import Product, ProductList



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://william:root1234@localhost/classicmodels'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'vinh'
api = Api(app)
db.init_app(app)

# @app.before_first_request
# def create_tables():
#     db.create_all()

jwt = JWT(app, authenticate, identity) # /auth


api.add_resource(Customer, '/api/v0/customers/<customerNumber>')
api.add_resource(Employee, '/api/v0/employees/<employeeNumber>')
api.add_resource(Office, '/api/v0/offices/<officeCode>')
api.add_resource(Orderdetail, '/api/v0/orderdetails/<orderNumber>')
api.add_resource(Order, '/api/v0/orders/<orderNumber>')
api.add_resource(Payment, '/api/v0/payments/<customerNumber>')
api.add_resource(Productline, '/api/v0/productlines/<productLine>')
api.add_resource(Product, '/api/v0/products/<productCode>')


api.add_resource(CustomerList, '/api/v0/customers')
api.add_resource(EmployeeList, '/api/v0/employees')
api.add_resource(OfficeList, '/api/v0/offices')
api.add_resource(OrderdetailList, '/api/v0/orderdetails')
api.add_resource(OrderList, '/api/v0/orders')
api.add_resource(PaymentList, '/api/v0/payments')
api.add_resource(ProductlineList, '/api/v0/productlines')
api.add_resource(ProductList, '/api/v0/products')


api.add_resource(UserRegister, '/register')


if __name__ == "__main__":
    app.run(port=5000, debug=True)