from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.payment import PaymentModel



class Payment(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument('checkNumber',
        type=str,
        required=True,
        help="This field cannot be left blank"
    )

    parser.add_argument('paymentDate',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('amount',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )


#    @jwt_required()
    def get(self, customerNumber):
        payment = PaymentModel.find_by_customerNumber(customerNumber)
        if payment:
            return payment.json()
        return {'message': 'payment not found'}, 404


    def post(self, customerNumber):
        if PaymentModel.find_by_customerNumber(customerNumber):
            return {'message': 'A payment with customerNumber "{}" already exists'.format(customerNumber)}, 400 # Something Wrong With The Request
        
        data = Payment.parser.parse_args()

        payment = PaymentModel(customerNumber, **data)

        try:
            payment.save_to_db()
        except:
            return {"message": "An Error occurred inserting the payment."}, 500 # Internal Server Error
        
        return payment.json(), 201

    @jwt_required()
    def delete(self, customerNumber):
        
        payment = PaymentModel.find_by_customerNumber(customerNumber)
        if payment:
            payment.delete_from_db()

        return {'message': 'payment deleted'}, 204


    def put(self, customerNumber):
        data = Payment.parser.parse_args()

        payment = PaymentModel.find_by_customerNumber(customerNumber)

        if payment is None:
            payment = PaymentModel(customerNumber, **data)
        else:
            payment.checkNumber = data['checkNumber']
            payment.paymentDate = data['paymentDate']
            payment.amount = data['amount']

        payment.save_to_db()

        return payment.json()


class PaymentList(Resource):
    def get(self):
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 25, type=int)

        items = PaymentModel.query

        for k, v in request.args.items():
            if k == 'checkNumber':
                items = items.filter_by(checkNumber=v)
            if k == 'paymentDate':
                items = items.filter_by(paymentDate=v)
            if k == 'amount':
                items = items.filter_by(amount=v)
            if k == 'customerNumber':
                items = items.filter_by(customerNumber=v)

            if k == 'sort':
                if ',' in v and '-' in v:
                    items = items.order_by(desc(v[1: v.find(',')]), v[v.find(',') + 1:])
                elif ',' in v:
                    items = items.order_by(v[: v.find(',')].strip(' +'), v[v.find(',') + 1:])
                elif '-' in v:
                    items = items.order_by(desc(v.strip('-')))
                else:
                    items = items.order_by(v.strip(' +'))
            else:
                items = items

        return {"customers": [customer.json() for customer in items.paginate(page=page, per_page=limit).items]}