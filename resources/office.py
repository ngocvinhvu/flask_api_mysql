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
            office.officeCode = data['officeCode']
            office.state = data['state']
            office.country = data['country']
            office.postalCode = data['postalCode']
            office.postalCode = data['territory']

        office.save_to_db()

        return office.json()


class OfficeList(Resource):
    def get(self):
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 25, type=int)
        sort = request.args.get('sort', type=str)
        filter_city = request.args.get('city', type=str)
        filter_phone = request.args.get('phone', type=str)

        if filter_city and filter_phone:
            items = OfficeModel.query.filter(OfficeModel.city == filter_city, OfficeModel.phone == filter_phone)
            return {"offices": [office.json() for office in items.paginate(page=page, per_page=limit).items]}

        elif filter_city:
            items = OfficeModel.query.filter(OfficeModel.city == filter_city)
            return {"offices": [office.json() for office in items.paginate(page=page, per_page=limit).items]}

        elif filter_phone:
            items = OfficeModel.query.filter(OfficeModel.phone == filter_phone)
            return {"offices": [office.json() for office in items.paginate(page=page, per_page=limit).items]}

        else:
            items = OfficeModel.query.paginate(page=page, per_page=limit)
            item_list = [office.json() for office in items.items]
            if sort:
                try:
                    if "-" in sort:
                        return {"office": sorted(item_list, key=lambda x: x[sort.strip('-')], reverse=True)}
                    else:
                        return {"office": sorted(item_list, key=lambda x: x[sort.strip(' +')], reverse=False)}
                except KeyError:
                    return {"message": "KeyError"}, 400
            return {"offices": [office.json() for office in items.items]}