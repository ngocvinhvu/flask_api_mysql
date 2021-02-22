from db import db


class ProductModel(db.Model):


    __tablename__ = "products"


    productCode = db.Column(db.String(15), primary_key=True)
    productName = db.Column(db.String(70))
    productLine = db.Column(db.String(50), db.ForeignKey('productlines.productLine'))
    productScale = db.Column(db.String(10))
    productVendor = db.Column(db.String(50))
    productDescription = db.Column(db.Text)
    quantityInStock = db.Column(db.Integer)
    buyPrice = db.Column(db.Float(precision=2))
    MSRP = db.Column(db.Float(precision=2))

    
    productlines = db.relationship("ProductlineModel")
    orderdetail = db.relationship("OrderdetailModel")


    def __init__(
        self,
        productCode,
        productName,
        productLine,
        productScale,
        productVendor,
        productDescription,
        quantityInStock,
        buyPrice,
        MSRP
    ):
        self.productCode = productCode
        self.productName = productName
        self.productLine = productLine
        self.productScale = productScale
        self.productVendor = productVendor
        self.productDescription = productDescription
        self.quantityInStock = quantityInStock
        self.buyPrice = buyPrice
        self.MSRP = MSRP

    def json(self):
        return {
            "productCode": self.productCode,
            "productName": self.productName,
            "productLine": self.productLine,
            "productScale": self.productScale,
            "productVendor": self.productVendor,
            "productDescription": self.productDescription,
            "quantityInStock": self.quantityInStock,
            "buyPrice": self.buyPrice,
            "MSRP": self.MSRP
        }


    @classmethod
    def find_by_productCode(cls, productCode):
        return cls.query.filter_by(
            productCode=productCode
        ).first()  # SELECT * FROM products WHERE productCode=productCode LIMIT 1


    def save_to_db(self):

        db.session.add(self)
        db.session.commit()


    def delete_from_db(self):

        db.session.delete(self)
        db.session.commit()
