from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.productline import ProductlineModel



class Productline(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument('textDescription',
        type=str
    )

    parser.add_argument('htmlDescription',
        type=str
    )

    parser.add_argument('image',
        type=str
    )


    def get(self, productLine):
        productline = ProductlineModel.find_by_productLine(productLine)
        if productline:
            return productline.json()
        return {'message': 'productline not found'}, 404


    def post(self, productLine):
        if ProductlineModel.find_by_productLine(productLine):
            return {'message': 'A productline with productLine "{}" already exists'.format(productLine)}, 400 # Something Wrong With The Request
        
        data = Productline.parser.parse_args()

        productline = ProductlineModel(productLine, **data)

        try:
            productline.save_to_db()
        except:
            return {"message": "An Error occurred inserting the productline."}, 500 # Internal Server Error
        
        return productline.json(), 201

    @jwt_required()
    def delete(self, productLine):
        
        productline = ProductlineModel.find_by_productLine(productLine)
        if productline:
            productline.delete_from_db()

        return {'message': 'productline deleted'}, 204


    def put(self, productLine):
        data = Productline.parser.parse_args()

        productline = ProductlineModel.find_by_productLine(productLine)

        if productline is None:
            productline = ProductlineModel(productLine, **data)
        else:
            productline.textDescription = data['textDescription']
            productline.htmlDescription = data['htmlDescription']
            productline.image = data['image']

        productline.save_to_db()

        return productline.json()


class ProductlineList(Resource):
    def get(self):
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 25, type=int)

        items = ProductlineModel.query

        for k, v in request.args.items():
            if k == 'productLine':
                items = items.filter_by(productLine=v)
            if k == 'textDescription':
                items = items.filter_by(textDescription=v)
            if k == 'htmlDescription':
                items = items.filter_by(htmlDescription=v)
            if k == 'image':
                items = items.filter_by(image=v)

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