from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.employee import EmployeeModel



class Employee(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument('lastName',
        type=str,
        required=True,
        help="This field cannot be left blank"
    )

    parser.add_argument('firstName',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('extension',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('email',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('officeCode',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('reportsTo',
        type=int
    )

    parser.add_argument('jobTitle',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )


#    @jwt_required()
    def get(self, employeeNumber):
        employee = EmployeeModel.find_by_employeeNumber(employeeNumber)
        if employee:
            return employee.json()
        return {'message': 'employee not found'}, 404


    def post(self, employeeNumber):
        if EmployeeModel.find_by_employeeNumber(employeeNumber):
            return {'message': 'A employee with employeeNumber "{}" already exists'.format(employeeNumber)}, 400 # Something Wrong With The Request
        
        data = Employee.parser.parse_args()

        employee = EmployeeModel(employeeNumber, **data)

        try:
            employee.save_to_db()
        except:
            return {"message": "An Error occurred inserting the employee."}, 500 # Internal Server Error
        
        return employee.json(), 201

    @jwt_required()
    def delete(self, employeeNumber):
        
        employee = EmployeeModel.find_by_employeeNumber(employeeNumber)
        if employee:
            employee.delete_from_db()

        return {'message': 'Employee deleted'}, 204


    def put(self, employeeNumber):
        data = Employee.parser.parse_args()

        employee = EmployeeModel.find_by_employeeNumber(employeeNumber)

        if employee is None:
            employee = EmployeeModel(employeeNumber, **data)
        else:
            employee.lastName = data['lastName']
            employee.firstName = data['firstName']
            employee.extension = data['extension']
            employee.email = data['email']
            employee.officeCode = data['officeCode']
            employee.reportsTo = data['reportsTo']
            employee.jobTitle = data['jobTitle']

        employee.save_to_db()

        return employee.json()


class EmployeeList(Resource):
    def get(self):
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 25, type=int)

        items = EmployeeModel.query

        for k, v in request.args.items():
            if k == 'employeeNumber':
                items = items.filter_by(employeeNumber=v)
            if k == 'lastName':
                items = items.filter_by(lastName=v)
            if k == 'firstName':
                items = items.filter_by(firstName=v)
            if k == 'extension':
                items = items.filter_by(extension=v)
            if k == 'email':
                items = items.filter_by(email=v)
            if k == 'officeCode':
                items = items.filter_by(officeCode=v)
            if k == 'reportsTo':
                items = items.filter_by(reportsTo=v)
            if k == 'jobTitle':
                items = items.filter_by(jobTitle=v)

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