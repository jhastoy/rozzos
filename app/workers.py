import datetime
from flask import Blueprint, Flask, jsonify, request, flash, url_for, redirect, render_template


bp_workers = Blueprint('workers', __name__, url_prefix='/workers')

@bp_workers.route('', methods=['GET', 'POST'])
def index():
    from .models import Worker
    from main import db
    
    if request.method == 'POST':
        worker = Worker(first_name=request.form.get('first_name'), last_name=request.form.get('last_name'))
        db.session.add(worker)
        db.session.commit()
    
    workers = Worker.query.all()

    return render_template('workers.html', workers=workers)


@bp_workers.route('<int:worker_id>', methods=['POST'])
def delete(worker_id):
    from .models import Worker
    from main import db
    worker = Worker.query.filter_by(id=worker_id).first()
    db.session.delete(worker)
    db.session.commit()
    
    return redirect(url_for('workers.index'))

    
    

    
    
    

    
