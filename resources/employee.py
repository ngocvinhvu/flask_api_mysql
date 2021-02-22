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
        sort = request.args.get('sort', type=str)
        filter_firstName = request.args.get('firstName', type=str)
        filter_reportsTo = request.args.get('reportsTo', type=str)

        if filter_firstName and filter_reportsTo:
            items = EmployeeModel.query.filter(EmployeeModel.firstName == filter_firstName, EmployeeModel.reportsTo == filter_reportsTo)
            return {"employees": [employee.json() for employee in items.paginate(page=page, per_page=limit).items]}

        elif filter_firstName:
            items = EmployeeModel.query.filter(EmployeeModel.firstName == filter_firstName)
            return {"employees": [employee.json() for employee in items.paginate(page=page, per_page=limit).items]}

        elif filter_reportsTo:
            items = EmployeeModel.query.filter(EmployeeModel.reportsTo == filter_reportsTo)
            return {"employees": [employee.json() for employee in items.paginate(page=page, per_page=limit).items]}

        else:
            items = EmployeeModel.query.paginate(page=page, per_page=limit)
            item_list = [employee.json() for employee in items.items]
            if sort:
                try:
                    if "-" in sort:
                        return {"employee": sorted(item_list, key=lambda x: x[sort.strip('-')], reverse=True)}
                    else:
                        return {"employee": sorted(item_list, key=lambda x: x[sort.strip(' +')], reverse=False)}
                except KeyError:
                    return {"message": "KeyError"}, 400
            return {"employees": [employee.json() for employee in items.items]}