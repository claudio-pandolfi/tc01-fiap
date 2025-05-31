from mongoengine import Document, ObjectIdField, StringField, IntField, FloatField

class Trading(Document):
    _id = ObjectIdField()
    product = StringField(required=True)
    type = StringField(required=True)
    year = IntField(required=True)
    amount = FloatField(precision=2)

    def to_dict(self):
        return {
            '_id': str(self._id),
            'product': self.product,
            'type': self.type,
            'year': self.year,
            'amount': self.amount
        }

