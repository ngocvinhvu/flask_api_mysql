from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from sqlalchemy import desc

from models.customer import CustomerModel



class Customer(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument('customerName',
        type=str,
        required=True,
        help="This field cannot be left blank"
    )

    parser.add_argument('contactLastName',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('contactFirstName',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('phone',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('addressLine1',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('addressLine2',
        type=str
    )

    parser.add_argument('city',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('state',
        type=str
    )

    parser.add_argument('postalCode',
        type=str
    )

    parser.add_argument('country',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('salesRepEmployeeNumber',
        type=int
    )

    parser.add_argument('creditLimit',
        type=float
    )


#    @jwt_required()
    def get(self, customerNumber):
        customer = CustomerModel.find_by_customerNumber(customerNumber)
        if customer:
            return customer.json()
        return {'message': 'customer not found'}, 404


    def post(self, customerNumber):
        if CustomerModel.find_by_customerNumber(customerNumber):
            return {'message': 'A customer with customerNumber "{}" already exists'.format(customerNumber)}, 400 # Something Wrong With The Request
        
        data = Customer.parser.parse_args()

        customer = CustomerModel(customerNumber, **data)

        try:
            customer.save_to_db()
        except:
            return {"message": "An Error occurred inserting the customer."}, 500 # Internal Server Error
        
        return customer.json(), 201

    @jwt_required()
    def delete(self, customerNumber):
        
        customer = CustomerModel.find_by_customerNumber(customerNumber)
        if customer:
            customer.delete_from_db()

        return {'message': 'Customer deleted'}, 204


    def put(self, customerNumber):
        data = Customer.parser.parse_args()

        customer = CustomerModel.find_by_customerNumber(customerNumber)

        if customer is None:
            customer = CustomerModel(customerNumber, **data)
        else:
            customer.customerName = data['customerName']
            customer.contactLastName = data['contactLastName']
            customer.contactFirstName = data['contactFirstName']
            customer.phone = data['phone']
            customer.addressLine1 = data['addressLine1']
            customer.addressLine2 = data['addressLine2']
            customer.city = data['city']
            customer.state = data['state']
            customer.postalCode = data['postalCode']
            customer.country = data['country']
            customer.salesRepEmployeeNumber = data['salesRepEmployeeNumber']
            customer.creditLimit = data['creditLimit']

        customer.save_to_db()

        return customer.json()


class CustomerList(Resource):
    def get(self):
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 25, type=int)

        items = CustomerModel.query

        for k, v in request.args.items():
            if k == 'customerNumber':
                items = items.filter_by(customerNumber=v)
            if k == 'customerName':
                items = items.filter_by(customerName=v)
            if k == 'contactLastName':
                items = items.filter_by(contactLastName=v)
            if k == 'contactFirstName':
                items = items.filter_by(contactFirstName=v)
            if k == 'phone':
                items = items.filter_by(phone=v)
            if k == 'addressLine1':
                items = items.filter_by(addressLine1=v)
            if k == 'addressLine2':
                items = items.filter_by(addressLine2=v)
            if k == 'city':
                items = items.filter_by(city=v)
            if k == 'state':
                items = items.filter_by(state=v)
            if k == 'country':
                items = items.filter_by(country=v)
            if k == 'salesRepEmployeeNumber':
                items = items.filter_by(salesRepEmployeeNumber=v)
            if k == 'creditLimit':
                items = items.filter_by(creditLimit=v)
            if k == 'postalCode':
                items = items.filter_by(postalCode=v)

            if k == 'sort':
                if ',' in v and '-' in v:
                    items = items.order_by(desc(v[1: v.find(',')]), v[v.find(',') + 1:])
                elif ',' in v:
                    items = items.order_by(v[: v.find(',')].strip(' +'), v[v.find(',') + 1:])
                elif '-' in v:
                    items = items.order_by(desc(v.strip('-')))
                elif '+' in v:
                    items = items.order_by(v.strip(' +'))
            else:
                items = items

        return {"customers": [customer.json() for customer in items.paginate(page=page, per_page=limit).items]}