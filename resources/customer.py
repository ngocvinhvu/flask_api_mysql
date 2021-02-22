from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

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
        sort = request.args.get('sort', type=str)
        filter_country = request.args.get('country', type=str)
        filter_contactFirstName = request.args.get('contactFirstName', type=str)

        if filter_country and filter_contactFirstName:
            items = CustomerModel.query.filter(CustomerModel.country == filter_country, CustomerModel.contactFirstName == filter_contactFirstName)
            return {"customers": [customer.json() for customer in items.paginate(page=page, per_page=limit).items]}

        elif filter_country:
            items = CustomerModel.query.filter(CustomerModel.country == filter_country)
            return {"customers": [customer.json() for customer in items.paginate(page=page, per_page=limit).items]}

        elif filter_contactFirstName:
            items = CustomerModel.query.filter(CustomerModel.contactFirstName == filter_contactFirstName)
            return {"customers": [customer.json() for customer in items.paginate(page=page, per_page=limit).items]}

        else:
            items = CustomerModel.query.paginate(page=page, per_page=limit)
            item_list = [customer.json() for customer in items.items]
            if sort:
                try:
                    if "-" in sort:
                        return {"customer": sorted(item_list, key=lambda x: x[sort.strip('-')], reverse=True)}
                    else:
                        return {"customer": sorted(item_list, key=lambda x: x[sort.strip(' +')], reverse=False)}
                except KeyError:
                    return {"message": "KeyError"}, 400
            return {"customers": [customer.json() for customer in items.items]}