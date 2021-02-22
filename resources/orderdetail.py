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
        sort = request.args.get('sort', type=str)
        filter_productCode = request.args.get('productCode', type=str)
        filter_quantityOrdered = request.args.get('quantityOrdered', type=str)

        if filter_productCode and filter_quantityOrdered:
            items = OrderdetailModel.query.filter(OrderdetailModel.productCode == filter_productCode, OrderdetailModel.quantityOrdered == filter_quantityOrdered)
            return {"orderdetails": [orderdetail.json() for orderdetail in items.paginate(page=page, per_page=limit).items]}

        elif filter_productCode:
            items = OrderdetailModel.query.filter(OrderdetailModel.productCode == filter_productCode)
            return {"orderdetails": [orderdetail.json() for orderdetail in items.paginate(page=page, per_page=limit).items]}

        elif filter_quantityOrdered:
            items = OrderdetailModel.query.filter(OrderdetailModel.quantityOrdered == filter_quantityOrdered)
            return {"orderdetails": [orderdetail.json() for orderdetail in items.paginate(page=page, per_page=limit).items]}

        else:
            items = OrderdetailModel.query.paginate(page=page, per_page=limit)
            item_list = [orderdetail.json() for orderdetail in items.items]
            if sort:
                try:
                    if "-" in sort:
                        return {"orderdetail": sorted(item_list, key=lambda x: x[sort.strip('-')], reverse=True)}
                    else:
                        return {"orderdetail": sorted(item_list, key=lambda x: x[sort.strip(' +')], reverse=False)}
                except KeyError:
                    return {"message": "KeyError"}, 400
            return {"orderdetails": [orderdetail.json() for orderdetail in items.items]}