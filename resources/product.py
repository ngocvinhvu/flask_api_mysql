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
            product.productCode = data['productCode']
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
        sort = request.args.get('sort', type=str)
        filter_productName = request.args.get('productName', type=str)
        filter_productLine = request.args.get('productLine', type=str)

        if filter_productName and filter_productLine:
            items = ProductModel.query.filter(ProductModel.productName == filter_productName, ProductModel.productLine == filter_productLine)
            return {"products": [product.json() for product in items.paginate(page=page, per_page=limit).items]}

        elif filter_productName:
            items = ProductModel.query.filter(ProductModel.productName == filter_productName)
            return {"products": [product.json() for product in items.paginate(page=page, per_page=limit).items]}

        elif filter_productLine:
            items = ProductModel.query.filter(ProductModel.productLine == filter_productLine)
            return {"products": [product.json() for product in items.paginate(page=page, per_page=limit).items]}

        else:
            items = ProductModel.query.paginate(page=page, per_page=limit)
            item_list = [product.json() for product in items.items]
            if sort:
                try:
                    if "-" in sort:
                        return {"product": sorted(item_list, key=lambda x: x[sort.strip('-')], reverse=True)}
                    else:
                        return {"product": sorted(item_list, key=lambda x: x[sort.strip(' +')], reverse=False)}
                except KeyError:
                    return {"message": "KeyError"}, 400
            return {"products": [product.json() for product in items.items]}