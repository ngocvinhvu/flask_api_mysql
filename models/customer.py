from db import db


class CustomerModel(db.Model):


    __tablename__ = "customers"


    customerNumber = db.Column(db.Integer, primary_key=True)
    customerName = db.Column(db.String(50))
    contactLastName = db.Column(db.String(50))
    contactFirstName = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    addressLine1 = db.Column(db.String(50))
    addressLine2 = db.Column(db.String(50))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    postalCode = db.Column(db.String(15))
    country = db.Column(db.String(50))
    salesRepEmployeeNumber = db.Column(db.Integer, db.ForeignKey('employees.employeeNumber'))
    creditLimit = db.Column(db.Float(precision=2))

    orders = db.relationship("OrderModel", lazy="dynamic")
    employee = db.relationship("EmployeeModel")
    payments = db.relationship("PaymentModel", lazy="dynamic")


    def __init__(
        self,
        customerNumber,
        customerName,
        contactLastName,
        contactFirstName,
        phone,
        addressLine1,
        addressLine2,
        city,
        state,
        postalCode,
        country,
        salesRepEmployeeNumber,
        creditLimit
    ):
        self.customerNumber = customerNumber
        self.customerName = customerName
        self.contactLastName = contactLastName
        self.contactFirstName = contactFirstName
        self.phone = phone
        self.addressLine1 = addressLine1
        self.addressLine2 = addressLine2
        self.city = city
        self.state = state
        self.postalCode = postalCode
        self.country = country
        self.salesRepEmployeeNumber = salesRepEmployeeNumber
        self.creditLimit = creditLimit


    def json(self):
        return {
            "customerNumber": self.customerNumber,
            "customerName": self.customerName,
            "contactLastName": self.contactLastName,
            "contactFirstName": self.contactFirstName,
            "phone": self.phone,
            "addressLine1": self.addressLine1,
            "addressLine2": self.addressLine2,
            "city": self.city,
            "state": self.state,
            "postalCode": self.postalCode,
            "country": self.country,
            "salesRepEmployeeNumber": self.salesRepEmployeeNumber,
            "creditLimit": self.creditLimit
        }


    @classmethod
    def find_by_customerNumber(cls, customerNumber):
        return cls.query.filter_by(
            customerNumber=customerNumber
        ).first()  # SELECT * FROM customers WHERE customerNumber=customerNumber LIMIT 1


    def save_to_db(self):

        db.session.add(self)
        db.session.commit()


    def delete_from_db(self):

        db.session.delete(self)
        db.session.commit()
