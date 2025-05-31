from mongoengine import Document, ObjectIdField, StringField, IntField, FloatField

class Production(Document):
    _id = ObjectIdField()
    product = StringField(required=True)
    type = StringField(required=True)
    year = IntField(required=True)
    quantity = IntField()

    def to_dict(self):
        return {
            '_id': str(self._id),
            'product': self.product,
            'type': self.type,
            'year': self.year,
            'quantity': self.quantity
        }

