from db import db


class PaymentModel(db.Model):


    __tablename__ = "payments"


    customerNumber = db.Column(db.Integer, db.ForeignKey('customers.customerNumber') ,primary_key=True)
    checkNumber = db.Column(db.String(50), primary_key=True)
    paymentDate = db.Column(db.DateTime)
    amount = db.Column(db.Float(precision=2))


    customer = db.relationship("CustomerModel")


    def __init__(
        self,
        customerNumber,
        checkNumber,
        paymentDate,
        amount
    ):
        self.customerNumber = customerNumber
        self.checkNumber = checkNumber
        self.paymentDate = paymentDate
        self.amount = amount


    def json(self):
        return {
            "customerNumber": self.customerNumber,
            "checkNumber": self.checkNumber,
            "paymentDate": str(self.paymentDate),
            "amount": self.amount
        }


    @classmethod
    def find_by_customerNumber(cls, customerNumber):
        return cls.query.filter_by(
            customerNumber=customerNumber
        ).first()  # SELECT * FROM payments WHERE customerNumber=customerNumber LIMIT 1


    def save_to_db(self):

        db.session.add(self)
        db.session.commit()


    def delete_from_db(self):

        db.session.delete(self)
        db.session.commit()
