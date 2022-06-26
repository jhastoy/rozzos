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


    weight = db.Column(db.Float, nullable=True)
    
class Weighing(Input):
    __mapper_args__ = {'polymorphic_identity': 'weighing'}

    id = db.Column(None, db.ForeignKey('input.id'), primary_key=True)
    type = db.Column(db.String(80), nullable=False)
    long_thin = db.Column(db.Float, nullable=False)
    long_thick = db.Column(db.Float, nullable=False)
    short_thin = db.Column(db.Float, nullable=False)
    short_thick = db.Column(db.Float, nullable=False)


class Working(Input):
    __mapper_args__ = {'polymorphic_identity': 'working'}

    id = db.Column(None, db.ForeignKey('input.id'), primary_key=True)
    hours = db.Column(db.Float, nullable=False)

