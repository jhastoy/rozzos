
from threading import local

from sqlalchemy import false
from main import db


class BaseTask(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(80), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    worker_id = db.Column(
        db.Integer, db.ForeignKey('worker.id'), nullable=True)
    inputs = db.relationship('Input', backref='task', lazy=False)

    def add(self, task):
        assert isinstance(task, BaseTask)
        assert task.type == self.type
        assert task.date == self.date

        for task_input in task.inputs:
            if task_input.type not in [task_input_yo.type for task_input_yo in self.inputs]:
                self.inputs.append(task_input)
            else:
                local_input = [
                    local_input for local_input in self.inputs if local_input.type == task_input.type][0]

                local_input.add(task_input)

    def to_dict(self):
        return {
            "date": self.date.strftime("%Y-%m-%d"),
            "inputs": [input.to_dict() for input in self.inputs],
        }
