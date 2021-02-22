from db import db


class EmployeeModel(db.Model):


    __tablename__ = "employees"


    employeeNumber = db.Column(db.Integer, primary_key=True)
    lastName = db.Column(db.String(50))
    firstName = db.Column(db.String(50))
    extension = db.Column(db.String(10))
    email = db.Column(db.String(100))
    officeCode = db.Column(db.String(10), db.ForeignKey('offices.officeCode'))
    reportsTo = db.Column(db.Integer, db.ForeignKey('employees.employeeNumber'))
    jobTitle = db.Column(db.String(50))


    customers = db.relationship("CustomerModel", lazy='dynamic')
    office = db.relationship("OfficeModel")


    def __init__(
        self,
        employeeNumber,
        lastName,
        firstName,
        extension,
        email,
        officeCode,
        reportsTo,
        jobTitle
    ):
        self.employeeNumber = employeeNumber
        self.lastName = lastName
        self.firstName = firstName
        self.extension = extension
        self.email = email
        self.officeCode = officeCode
        self.reportsTo = reportsTo
        self.jobTitle = jobTitle


    def json(self):
        return {
            "employeeNumber": self.employeeNumber,
            "lastName": self.lastName,
            "firstName": self.firstName,
            "extension": self.extension,
            "email": self.email,
            "officeCode": self.officeCode,
            "reportsTo": self.reportsTo,
            "jobTitle": self.jobTitle
        }


    @classmethod
    def find_by_employeeNumber(cls, employeeNumber):
        return cls.query.filter_by(
            employeeNumber=employeeNumber
        ).first()  # SELECT * FROM employees WHERE employeeNumber=employeeNumber LIMIT 1


    def save_to_db(self):

        db.session.add(self)
        db.session.commit()


    def delete_from_db(self):

        db.session.delete(self)
        db.session.commit()
