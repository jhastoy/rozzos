from wsgiref.validate import InputWrapper
from main import db


class Input(db.Model):
    __tablename__ = 'input'

    id = db.Column(db.Integer, primary_key=True)
    input_type = db.Column(db.String(80), nullable=False)
    __mapper_args__ = {'polymorphic_on': input_type}
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)


class Loose(Input):
    __mapper_args__ = {'polymorphic_identity': 'loose'}
    id = db.Column(None, db.ForeignKey('input.id'), primary_key=True)
    type = db.Column(db.String(80), nullable=False)
    weight = db.Column(db.Float, nullable=True)

    def add(self, input):
        assert isinstance(input, Loose)
        assert input.type == self.type

        self.weight += input.weight

    def to_dict(self):
        return [
            {
                "label": "weight",
                "value": self.weight
            }
        ]


class Weighing(Input):
    __mapper_args__ = {'polymorphic_identity': 'weighing'}

    id = db.Column(None, db.ForeignKey('input.id'), primary_key=True)
    type = db.Column(db.String(80), nullable=False)
    long_thin = db.Column(db.Float, nullable=False)
    long_thick = db.Column(db.Float, nullable=False)
    short_thin = db.Column(db.Float, nullable=False)
    short_thick = db.Column(db.Float, nullable=False)

    def add(self, input):
        assert isinstance(input, Weighing)
        assert input.type == self.type

        self.long_thin += input.long_thin
        self.long_thick += input.long_thick
        self.short_thin += input.short_thin
        self.short_thick += input.short_thick

    def to_dict(self):

        return [
            {"label": "long_thin", "value": self.long_thin},
            {"label": "long_thick", "value": self.long_thick},
            {"label": "short_thin", "value": self.short_thin},
            {"label": "short_thick", "value": self.short_thick}
        ]


class Working(Input):
    __mapper_args__ = {'polymorphic_identity': 'working'}

    id = db.Column(None, db.ForeignKey('input.id'), primary_key=True)
    type = db.Column(db.String(80), nullable=False)

    hours = db.Column(db.Float, nullable=False)

    def add(self, input):
        assert isinstance(input, Working)
        assert input.type == self.type

        self.hours += input.hours

    def to_dict(self):
        return [{"label": "hours", "value": self.hours}]


class Number(Input):
    __mapper_args__ = {'polymorphic_identity': 'number'}

    id = db.Column(None, db.ForeignKey('input.id'), primary_key=True)
    type = db.Column(db.String(80), nullable=False)

    number = db.Column(db.Float, nullable=False)

    def add(self, input):
        assert isinstance(input, Number)
        assert input.type == self.type

        self.number += input.number

    def to_dict(self):
        return [{"label": "number", "value": self.number}]
