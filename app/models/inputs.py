from wsgiref.validate import InputWrapper
from main import db, config


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
        self.total = self.long_thin + self.long_thick + self.short_thin + self.short_thick

    def to_dict(
            self):
        if not hasattr(self, 'total'):
            self.total = self.long_thin + self.long_thick + self.short_thin + self.short_thick

        return [
            {"label": "total", "value": round(
                self.total, 2), "straws": round(self.long_thick / config['long_thick_weight'] + self.long_thin / config['long_thin_weight'] + self.short_thin / config['short_thin_weight'] + self.long_thin / config['long_thin_weight'])},
            {"label": "long_thin", "value": round(self.long_thin, 2), 'percentage': round(
                (self.long_thin / self.total) * 100 if self.total != 0 else 0, 2),
             'straws': round(self.long_thin / config['long_thin_weight'])},
            {"label": "long_thick", "value": round(self.long_thick, 2),
             'percentage': round((self.long_thick / self.total) * 100 if self.total != 0 else 0, 2),
             'straws': round(self.long_thick / config['long_thick_weight'])},
            {"label": "short_thin", "value": round(self.short_thin, 2),
             'percentage': round((self.short_thin / self.total) * 100 if self.total != 0 else 0, 2),
             'straws': round(self.short_thin / config['short_thin_weight'])},
            {"label": "short_thick", "value": round(self.short_thick , 2),
             'percentage': round((self.short_thick / self.total) * 100 if self.total != 0 else 0, 2),
             'straws': round(self.short_thick / config['short_thick_weight'])},

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
