from db import db


class ProductlineModel(db.Model):


    __tablename__ = "productlines"


    productLine = db.Column(db.String(50), primary_key=True)
    textDescription = db.Column(db.String(400))
    htmlDescription = db.Column(db.Text)
    image = db.Column(db.String(50))


    product = db.relationship("ProductModel")


    def __init__(
        self,
        productLine,
        textDescription,
        htmlDescription
    ):
        self.productLine = productLine
        self.textDescription = textDescription
        self.htmlDescription = htmlDescription
        self.image = image


    def json(self):
        return {
            "productLine": self.productLine,
            "textDescription": self.textDescription,
            "htmlDescription": str(self.htmlDescription),
            "image": str(self.image)
        }


    @classmethod
    def find_by_productLine(cls, productLine):
        return cls.query.filter_by(
            productLine=productLine
        ).first()  # SELECT * FROM productlines WHERE productLine=productLine LIMIT 1


    def save_to_db(self):

        db.session.add(self)
        db.session.commit()


    def delete_from_db(self):

        db.session.delete(self)
        db.session.commit()
