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


#    @jwt_required()
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
        sort = request.args.get('sort', type=str)
        filter_textDescription = request.args.get('textDescription', type=str)
        filter_htmlDescription = request.args.get('htmlDescription', type=str)

        if filter_textDescription and filter_htmlDescription:
            items = ProductlineModel.query.filter(ProductlineModel.textDescription == filter_textDescription, ProductlineModel.htmlDescription == filter_htmlDescription)
            return {"productlines": [productline.json() for productline in items.paginate(page=page, per_page=limit).items]}

        elif filter_textDescription:
            items = ProductlineModel.query.filter(ProductlineModel.textDescription == filter_textDescription)
            return {"productlines": [productline.json() for productline in items.paginate(page=page, per_page=limit).items]}

        elif filter_htmlDescription:
            items = ProductlineModel.query.filter(ProductlineModel.htmlDescription == filter_htmlDescription)
            return {"productlines": [productline.json() for productline in items.paginate(page=page, per_page=limit).items]}

        else:
            items = ProductlineModel.query.paginate(page=page, per_page=limit)
            item_list = [productline.json() for productline in items.items]
            if sort:
                try:
                    if "-" in sort:
                        return {"productline": sorted(item_list, key=lambda x: x[sort.strip('-')], reverse=True)}
                    else:
                        return {"productline": sorted(item_list, key=lambda x: x[sort.strip(' +')], reverse=False)}
                except KeyError:
                    return {"message": "KeyError"}, 400
            return {"productlines": [productline.json() for productline in items.items]}