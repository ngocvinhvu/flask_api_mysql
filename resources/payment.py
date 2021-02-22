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
        sort = request.args.get('sort', type=str)
        filter_checkNumber = request.args.get('checkNumber', type=str)
        filter_paymentDate = request.args.get('paymentDate', type=str)

        if filter_checkNumber and filter_paymentDate:
            items = PaymentModel.query.filter(PaymentModel.checkNumber == filter_checkNumber, PaymentModel.paymentDate == filter_paymentDate)
            return {"payments": [payment.json() for payment in items.paginate(page=page, per_page=limit).items]}

        elif filter_checkNumber:
            items = PaymentModel.query.filter(PaymentModel.checkNumber == filter_checkNumber)
            return {"payments": [payment.json() for payment in items.paginate(page=page, per_page=limit).items]}

        elif filter_paymentDate:
            items = PaymentModel.query.filter(PaymentModel.paymentDate == filter_paymentDate)
            return {"payments": [payment.json() for payment in items.paginate(page=page, per_page=limit).items]}

        else:
            items = PaymentModel.query.paginate(page=page, per_page=limit)
            item_list = [payment.json() for payment in items.items]
            if sort:
                try:
                    if "-" in sort:
                        return {"payment": sorted(item_list, key=lambda x: x[sort.strip('-')], reverse=True)}
                    else:
                        return {"payment": sorted(item_list, key=lambda x: x[sort.strip(' +')], reverse=False)}
                except KeyError:
                    return {"message": "KeyError"}, 400
            return {"payments": [payment.json() for payment in items.items]}