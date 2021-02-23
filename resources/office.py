from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.office import OfficeModel



class Office(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument('city',
        type=str,
        required=True,
        help="This field cannot be left blank"
    )

    parser.add_argument('phone',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('addressLine1',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('addressLine2',
        type=str
    )

    parser.add_argument('state',
        type=str
    )

    parser.add_argument('country',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('postalCode',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('territory',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

#    @jwt_required()
    def get(self, officeCode):
        office = OfficeModel.find_by_officeCode(officeCode)
        if office:
            return office.json()
        return {'message': 'office not found'}, 404


    def post(self, officeCode):
        if OfficeModel.find_by_officeCode(officeCode):
            return {'message': 'A office with officeCode "{}" already exists'.format(officeCode)}, 400 # Something Wrong With The Request
        
        data = Office.parser.parse_args()

        office = OfficeModel(officeCode, **data)

        try:
            office.save_to_db()
        except:
            return {"message": "An Error occurred inserting the office."}, 500 # Internal Server Error
        
        return office.json(), 201
        

    @jwt_required()
    def delete(self, officeCode):
        
        office = OfficeModel.find_by_officeCode(officeCode)
        if office:
            office.delete_from_db()

        return {'message': 'Office deleted'}, 204


    def put(self, officeCode):
        data = Office.parser.parse_args()

        office = OfficeModel.find_by_officeCode(officeCode)

        if office is None:
            office = OfficeModel(officeCode, **data)
        else:
            office.city = data['city']
            office.phone = data['phone']
            office.addressLine1 = data['addressLine1']
            office.addressLine2 = data['addressLine2']
            office.state = data['state']
            office.country = data['country']
            office.postalCode = data['postalCode']
            office.territory = data['territory']

        office.save_to_db()

        return office.json()


class OfficeList(Resource):
    def get(self):
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 25, type=int)

        items = OfficeModel.query

        for k, v in request.args.items():
            if k == 'officeCode':
                items = items.filter_by(officeCode=v)
            if k == 'city':
                items = items.filter_by(city=v)
            if k == 'addressLine1':
                items = items.filter_by(addressLine1=v)
            if k == 'addressLine2':
                items = items.filter_by(addressLine2=v)
            if k == 'phone':
                items = items.filter_by(phone=v)
            if k == 'state':
                items = items.filter_by(state=v)
            if k == 'country':
                items = items.filter_by(country=v)
            if k == 'territory':
                items = items.filter_by(territory=v)
            if k == 'postalCode':
                items = items.filter_by(postalCode=v)

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