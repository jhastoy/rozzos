
from main import db


class BaseTask(db.Model):
    __tablename__ = 'task'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(80), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    worker_id = db.Column(db.Integer, db.ForeignKey('worker.id'), nullable=True)
    inputs = db.relationship('Input', backref='task', lazy=True)
   
