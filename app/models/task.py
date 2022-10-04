
from threading import local

from sqlalchemy import false
from app.models.inputs import Weighing, Working
from main import db


class BaseTask(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(80), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    worker_id = db.Column(
        db.Integer, db.ForeignKey('worker.id'), nullable=True)
    inputs = db.relationship('Input', backref='task', lazy=False)
    workers = {}

    def add(self, task, period=False):
        assert isinstance(task, BaseTask)
        assert task.type == self.type
        if not period:
            assert task.date == self.date

        
        if task.type not in self.workers.keys():
            self.workers[task.type] = []
        
        self.workers[task.type].append(task.worker_id)
        
        
        for i, task_input in enumerate(task.inputs):
            if task_input.type not in [task_input_yo.type for task_input_yo in self.inputs]:
                self.inputs.append(task_input)
            else:
                local_input = [
                    local_input for local_input in self.inputs if local_input.type == task_input.type][0]

                local_input.add(task_input)

    def to_dict(self, period=False):
        total_weight = 0
        total_hour = 0
        if self.type in self.workers.keys():
            num_workers = len(set(self.workers[self.type]))
            for input in self.inputs:
                if type(input) is Weighing and hasattr(input, "total"):
                    print('coucou')
                    total_weight += input.total
                if type(input) is Working and hasattr(input, "hours"):
                    total_hour += input.hours
        else:
            num_workers = 0
       
        
        
        weight_by_hour = round(total_weight / total_hour, 2) if total_hour != 0 else 0
        weight_by_worker = round(total_weight / num_workers,2) if num_workers != 0 else 0
        weight_by_worker_by_hour = round(total_weight / num_workers / total_hour, 2) if num_workers != 0 and total_hour != 0 else 0
        
        dictio = {
            "data": {"weight_by_hour": weight_by_hour, "weight_by_operator": weight_by_worker, "weight_by_operator_by_hour": weight_by_worker_by_hour, 'operators':  num_workers},
            "inputs": [input.to_dict() for input in self.inputs],
        }
        if not period:
            dictio.update({"date": self.date.strftime("%Y-%m-%d")})

        return dictio
