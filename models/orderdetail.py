from db import db


class OrderdetailModel(db.Model):


    __tablename__ = "orderdetails"


    orderNumber = db.Column(db.Integer, db.ForeignKey('orders.orderNumber'), primary_key=True)
    productCode = db.Column(db.String(15), db.ForeignKey('products.productCode'), primary_key=True)
    quantityOrdered = db.Column(db.String(11))
    priceEach = db.Column(db.Float(precision=2))
    orderLineNumber = db.Column(db.Integer)


    order = db.relationship("OrderModel")
    products = db.relationship("ProductModel")


    def __init__(
        self,
        orderNumber,
        productCode,
        quantityOrdered,
        priceEach,
        orderLineNumber
    ):
        self.orderNumber = orderNumber
        self.productCode = productCode
        self.quantityOrdered = quantityOrdered
        self.priceEach = priceEach
        self.orderLineNumber = orderLineNumber


    def json(self):
        return {
            "orderNumber": self.orderNumber,
            "productCode": self.productCode,
            "quantityOrdered": self.quantityOrdered,
            "priceEach": self.priceEach,
            "orderLineNumber": self.orderLineNumber
        }


    @classmethod
    def find_by_orderNumber(cls, orderNumber):
        return cls.query.filter_by(
            orderNumber=orderNumber
        ).first()  # SELECT * FROM oderdetails WHERE orderNumber=orderNumber LIMIT 1


    def save_to_db(self):

        db.session.add(self)
        db.session.commit()


    def delete_from_db(self):

        db.session.delete(self)
        db.session.commit()
