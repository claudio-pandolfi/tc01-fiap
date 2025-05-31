from mongoengine import Document, ObjectIdField, StringField, IntField, FloatField

class Exportation(Document):
    _id = ObjectIdField()
    country = StringField(required=True)
    product = StringField(required=True)
    year = IntField(required=True)
    quantity = IntField(required=True)
    amount = FloatField(precision=2)

    def to_dict(self):
        return {
            '_id': str(self._id),
            'country': self.country,
            'product': self.product,
            'year': self.year,
            'quantity': self.quantity,
            'amount': self.amount
        }

