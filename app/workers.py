import datetime
from flask import Blueprint, Flask, jsonify, request, flash, url_for, redirect, render_template


bp_workers = Blueprint('workers', __name__, url_prefix='/workers')

@bp_workers.route('', methods=['GET', 'POST'])
def index():
    from .models import Worker
    from main import db
    
    if request.method == 'POST':
        worker = Worker(first_name=request.form.get('first_name'), last_name=request.form.get('last_name'), num_worker=request.form.get('num_worker'))
        db.session.add(worker)
        db.session.commit()
    
    workers = Worker.query.order_by(Worker.num_worker).all()

    return render_template('workers.html', workers=workers)


@bp_workers.route('<int:worker_id>', methods=['POST'])
def delete(worker_id):
    from .models import Worker
    from main import db
    print(worker_id)
    worker = Worker.query.filter_by(id=worker_id).first()
    print(worker)
    db.session.delete(worker)
    db.session.commit()
    
    return redirect(url_for('workers.index'))

    
    

    
    
    

    
