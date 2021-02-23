from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.product import ProductModel



class Product(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument('productName',
        type=str,
        required=True,
        help="This field cannot be left blank"
    )

    parser.add_argument('productLine',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('productScale',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('productVendor',
        type=str
    )

    parser.add_argument('productDescription',
        type=str
    )

    parser.add_argument('quantityInStock',
        type=int,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('buyPrice',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('MSRP',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

#    @jwt_required()
    def get(self, productCode):
        product = ProductModel.find_by_productCode(productCode)
        if product:
            return product.json()
        return {'message': 'product not found'}, 404


    def post(self, productCode):
        if ProductModel.find_by_productCode(productCode):
            return {'message': 'A product with productCode "{}" already exists'.format(productCode)}, 400 # Something Wrong With The Request
        
        data = Product.parser.parse_args()

        product = ProductModel(productCode, **data)

        try:
            product.save_to_db()
        except:
            return {"message": "An Error occurred inserting the product."}, 500 # Internal Server Error
        
        return product.json(), 201

    @jwt_required()
    def delete(self, productCode):
        
        product = ProductModel.find_by_productCode(productCode)
        if product:
            product.delete_from_db()

        return {'message': 'product deleted'}, 204


    def put(self, productCode):
        data = Product.parser.parse_args()

        product = ProductModel.find_by_productCode(productCode)

        if product is None:
            product = ProductModel(productCode, **data)
        else:
            product.productName = data['productName']
            product.productLine = data['productLine']
            product.productScale = data['productScale']
            product.productVendor = data['productVendor']
            product.productDescription = data['productDescription']
            product.quantityInStock = data['quantityInStock']
            product.buyPrice = data['buyPrice']
            product.MSRP = data['MSRP']

        product.save_to_db()

        return product.json()


class ProductList(Resource):
    def get(self):
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 25, type=int)

        items = ProductModel.query

        for k, v in request.args.items():
            if k == 'productCode':
                items = items.filter_by(productCode=v)
            if k == 'productLine':
                items = items.filter_by(productLine=v)
            if k == 'productScale':
                items = items.filter_by(productScale=v)
            if k == 'productVendor':
                items = items.filter_by(productVendor=v)
            if k == 'productDescription':
                items = items.filter_by(productDescription=v)
            if k == 'quantityInStock':
                items = items.filter_by(quantityInStock=v)
            if k == 'buyPrice':
                items = items.filter_by(buyPrice=v)
            if k == 'MSRP':
                items = items.filter_by(MSRP=v)

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