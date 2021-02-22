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
        sort = request.args.get('sort', type=str)
        filter_orderDate = request.args.get('orderDate', type=str)
        filter_requiredDate = request.args.get('requiredDate', type=str)

        if filter_orderDate and filter_requiredDate:
            items = OrderModel.query.filter(OrderModel.orderDate == filter_orderDate, OrderModel.requiredDate == filter_requiredDate)
            return {"orders": [order.json() for order in items.paginate(page=page, per_page=limit).items]}

        elif filter_orderDate:
            items = OrderModel.query.filter(OrderModel.orderDate == filter_orderDate)
            return {"orders": [order.json() for order in items.paginate(page=page, per_page=limit).items]}

        elif filter_requiredDate:
            items = OrderModel.query.filter(OrderModel.requiredDate == filter_requiredDate)
            return {"orders": [order.json() for order in items.paginate(page=page, per_page=limit).items]}

        else:
            items = OrderModel.query.paginate(page=page, per_page=limit)
            item_list = [order.json() for order in items.items]
            if sort:
                try:
                    if "-" in sort:
                        return {"order": sorted(item_list, key=lambda x: x[sort.strip('-')], reverse=True)}
                    else:
                        return {"order": sorted(item_list, key=lambda x: x[sort.strip(' +')], reverse=False)}
                except KeyError:
                    return {"message": "KeyError"}, 400
            return {"orders": [order.json() for order in items.items]}