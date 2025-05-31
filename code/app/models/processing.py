from mongoengine import Document, ObjectIdField, StringField, IntField, FloatField

class Processing(Document):
    _id = ObjectIdField()
    product = StringField(required=True)
    cultivation = StringField(required=True)
    classification = StringField(required=True)
    year = IntField(required=True)
    quantity = IntField()

    def to_dict(self):
        return {
            '_id': str(self._id),
            'product': self.product,
            'cultivation': self.cultivation,
            'classification': self.classification,
            'year': self.year,
            'quantity': self.quantity
        }

