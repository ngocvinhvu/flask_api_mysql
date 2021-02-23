from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.orderdetail import OrderdetailModel



class Orderdetail(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument('productCode',
        type=str,
        required=True,
        help="This field cannot be left blank"
    )

    parser.add_argument('quantityOrdered',
        type=int,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('priceEach',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('orderLineNumber',
        type=int,
        required=True,
        help="This field cannot be left blank!"
    )


#    @jwt_required()
    def get(self, orderNumber):
        orderdetail = OrderdetailModel.find_by_orderNumber(orderNumber)
        if orderdetail:
            return orderdetail.json()
        return {'message': 'order not found'}, 404


    def post(self, orderNumber):
        if OrderdetailModel.find_by_orderNumber(orderNumber):
            return {'message': 'A order with orderNumber "{}" already exists'.format(orderNumber)}, 400 # Something Wrong With The Request
        
        data = Orderdetail.parser.parse_args()

        orderdetail = OrderdetailModel(orderNumber, **data)

        try:
            orderdetail.save_to_db()
        except:
            return {"message": "An Error occurred inserting the order."}, 500 # Internal Server Error
        
        return orderdetail.json(), 201

    def delete(self, orderNumber):
        
        orderdetail = OrderdetailModel.find_by_orderNumber(orderNumber)
        if orderdetail:
            orderdetail.delete_from_db()

        return {'message': 'Order deleted'}, 204


    def put(self, orderNumber):
        data = Orderdetail.parser.parse_args()

        orderdetail = OrderdetailModel.find_by_orderNumber(orderNumber)

        if orderdetail is None:
            orderdetail = OrderdetailModel(orderNumber, **data)
        else:
            orderdetail.productCode = data['productCode']
            orderdetail.quantityOrdered = data['quantityOrdered']
            orderdetail.priceEach = data['priceEach']
            orderdetail.orderLineNumber = data['orderLineNumber']
            orderdetail.customerNumber = data['customerNumber']

        orderdetail.save_to_db()

        return orderdetail.json()


class OrderdetailList(Resource):
    def get(self):
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 25, type=int)

        items = OrderdetailModel.query

        for k, v in request.args.items():
            if k == 'orderNumber':
                items = items.filter_by(orderNumber=v)
            if k == 'productCode':
                items = items.filter_by(productCode=v)
            if k == 'quantityOrdered':
                items = items.filter_by(quantityOrdered=v)
            if k == 'priceEach':
                items = items.filter_by(priceEach=v)
            if k == 'orderLineNumber':
                items = items.filter_by(orderLineNumber=v)
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