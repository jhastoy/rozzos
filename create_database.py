from main import db
from app.models.task import BaseTask
from app.models.inputs import *
from app.models.worker import Worker

import os
import json

def main():

    db.create_all()
        
    for i in range(1, 10):
        worker = Worker(first_name='Worker {}'.format(i), last_name='Lastname {}'.format(i))
        db.session.add(worker)
        db.session.commit()
 

if __name__ == '__main__':
    main()