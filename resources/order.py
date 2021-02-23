from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.order import OrderModel



class Order(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument('orderDate',
        type=str,
        required=True,
        help="This field cannot be left blank"
    )

    parser.add_argument('requiredDate',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('shippedDate',
        type=str
    )

    parser.add_argument('status',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('customerNumber',
        type=int,
        required=True,
        help="This field cannot be left blank!"
    )


#    @jwt_required()
    def get(self, orderNumber):
        order = OrderModel.find_by_orderNumber(orderNumber)
        if order:
            return order.json()
        return {'message': 'order not found'}, 404


    def post(self, orderNumber):
        if OrderModel.find_by_orderNumber(orderNumber):
            return {'message': 'A order with orderNumber "{}" already exists'.format(orderNumber)}, 400 # Something Wrong With The Request
        
        data = Order.parser.parse_args()

        order = OrderModel(orderNumber, **data)

        try:
            order.save_to_db()
        except:
            return {"message": "An Error occurred inserting the order."}, 500 # Internal Server Error
        
        return order.json(), 201

    def delete(self, orderNumber):
        
        order = OrderModel.find_by_orderNumber(orderNumber)
        if order:
            order.delete_from_db()

        return {'message': 'Order deleted'}, 204


    def put(self, orderNumber):
        data = Order.parser.parse_args()

        order = OrderModel.find_by_orderNumber(orderNumber)

        if order is None:
            order = OrderModel(orderNumber, **data)
        else:
            order.orderDate = data['orderDate']
            order.requiredDate = data['requiredDate']
            order.shippedDate = data['shippedDate']
            order.status = data['status']
            order.customerNumber = data['customerNumber']

        order.save_to_db()

        return order.json()


class OrderList(Resource):
    def get(self):
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 25, type=int)

        items = OrderModel.query

        for k, v in request.args.items():
            if k == 'orderNumber':
                items = items.filter_by(orderNumber=v)
            if k == 'requiredDate':
                items = items.filter_by(requiredDate=v)
            if k == 'shippedDate':
                items = items.filter_by(shippedDate=v)
            if k == 'status':
                items = items.filter_by(status=v)
            if k == 'orderDate':
                items = items.filter_by(orderDate=v)
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