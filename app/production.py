import datetime
from flask import Blueprint, Flask, jsonify, request, flash, url_for, redirect, render_template

bp_production = Blueprint('production', __name__, url_prefix='/production')

@bp_production.route('', methods=['GET'])
def index():
    print(request.method)
    from .models.worker import Worker
  
    dt = datetime.datetime.now()
    date = dt.strftime("%Y-%m-%d")
    return redirect(url_for('production.index_date', date=date))


@bp_production.route('/<date>', methods=['GET'])
def index_date(date):
    
    from .models.worker import Worker
    from .models.task import BaseTask
    from main import db
    from main import config
    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    
    tasks = BaseTask.query.all()
    
    workers_pending = Worker.query.filter(~Worker.tasks.any(BaseTask.date == date)).all()
    workers_done = Worker.query.filter(Worker.tasks.any(BaseTask.date == date)).all()

    
    return render_template('production.html', workers_pending=workers_pending, workers_done=workers_done, prev_date=(date - datetime.timedelta(1)).strftime('%Y-%m-%d'),  next_date=(date + datetime.timedelta(1)).strftime('%Y-%m-%d'), date=date.strftime('%Y-%m-%d'),config=config)

        
@bp_production.route('/<date>/<int:worker_id>', methods=['GET','POST'])
def post_worker(worker_id, date):
    from .models.task import BaseTask
    from .models.inputs import Weighing, Loose, Working

    from .models.worker import Worker
    from main import config, db
    
 
    
    if request.method == 'POST':
        worker = Worker.query.filter_by(id=worker_id).first()
        
        print(request.form)
        task_id = request.form.get('task')
        
        task = [task for task in config['tasks'] if task['id'] == task_id][0]

        task_obj = BaseTask(type=task['type'], date=datetime.datetime.strptime(date, '%Y-%m-%d'), worker_id=worker_id)
        
        for item in task['inputs']:
            if item['type'] == 'time':
                task_obj.inputs.append(Working(hours=request.form.get('time')))
            elif item['type'] == 'weight':
                print(request.form)
                task_obj.inputs.append(Weighing(type=item['id'],  
                                                   long_thin=request.form.get('{}[long][thin]'.format(item['id'])),
                                                   long_thick=request.form.get('{}[long][thick]'.format(item['id'])), 
                                                   short_thin=request.form.get('{}[short][thin]'.format(item['id'])), 
                                                   short_thick=request.form.get('{}[short][thick]'.format(item['id']))))
            elif item['type'] == 'loose':
                task_obj.inputs.append(Loose(weight=request.form.get(item['type'])))
            
        worker.tasks.append(task_obj)
        db.session.commit()
        
        
    return redirect(url_for('production.index_date',date=date))
    
    

    
    
    

    
