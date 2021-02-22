from db import db


class OrderModel(db.Model):


    __tablename__ = "orders"


    orderNumber = db.Column(db.Integer, primary_key=True)
    orderDate = db.Column(db.DateTime)
    requiredDate = db.Column(db.DateTime)
    shippedDate = db.Column(db.DateTime)
    status = db.Column(db.String(50))
    comments = db.Column(db.Text)
    customerNumber = db.Column(db.Integer, db.ForeignKey('customers.customerNumber'))


    customer = db.relationship("CustomerModel")
    orderdetails = db.relationship("OrderdetailModel", lazy="dynamic")


    def __init__(
        self,
        orderNumber,
        orderDate,
        requiredDate,
        shippedDate,
        status,
        comments,
        customerNumber
    ):
        self.orderNumber = orderNumber
        self.orderDate = orderDate
        self.requiredDate = requiredDate
        self.shippedDate = shippedDate
        self.status = status
        self.comments = comments
        self.customerNumber = customerNumber


    def json(self):
        return {
            "orderNumber": self.orderNumber,
            "orderDate": str(self.orderDate),
            "requiredDate": str(self.requiredDate),
            "shippedDate": str(self.shippedDate),
            "status": self.status,
            "comments": self.comments,
            "customerNumber": self.customerNumber
        }


    @classmethod
    def find_by_orderNumber(cls, orderNumber):
        return cls.query.filter_by(
            orderNumber=orderNumber
        ).first()  # SELECT * FROM oders WHERE orderNumber=orderNumber LIMIT 1


    def save_to_db(self):

        db.session.add(self)
        db.session.commit()


    def delete_from_db(self):

        db.session.delete(self)
        db.session.commit()
