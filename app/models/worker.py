from main import db


class Worker(db.Model):
    __tablename__ = 'worker'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    num_worker = db.Column(db.Integer, nullable=False)
    tasks = db.relationship('BaseTask', backref='worker')
