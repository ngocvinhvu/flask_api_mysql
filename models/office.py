from db import db


class OfficeModel(db.Model):


    __tablename__ = "offices"


    officeCode = db.Column(db.String(10), primary_key=True)
    city = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    addressLine1 = db.Column(db.String(50))
    addressLine2 = db.Column(db.String(50))
    state = db.Column(db.String(50))
    country = db.Column(db.String(50))
    postalCode = db.Column(db.String(15))
    territory = db.Column(db.String(10))


    employees = db.relationship("EmployeeModel", lazy="dynamic")


    def __init__(
        self,
        officeCode,
        city,
        phone,
        addressLine1,
        addressLine2,
        state,
        country,
        postalCode,
        territory
    ):
        self.officeCode = officeCode
        self.city = city
        self.phone = phone
        self.addressLine1 = addressLine1
        self.addressLine2 = addressLine2
        self.state = state
        self.country = country
        self.postalCode = postalCode
        self.territory = territory

    def json(self):
        return {
            "officeCode": self.officeCode,
            "city": self.city,
            "phone": self.phone,
            "addressLine1": self.addressLine1,
            "addressLine2": self.addressLine2,
            "state": self.state,
            "country": self.country,
            "postalCode": self.postalCode,
            "territory": self.territory
        }


    @classmethod
    def find_by_officeCode(cls, officeCode):
        return cls.query.filter_by(
            officeCode=officeCode
        ).first()  # SELECT * FROM offices WHERE officeCode=officeCode LIMIT 1


    def save_to_db(self):

        db.session.add(self)
        db.session.commit()


    def delete_from_db(self):

        db.session.delete(self)
        db.session.commit()
