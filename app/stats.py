import datetime
import json
from flask import Blueprint, Flask, jsonify, request, flash, url_for, redirect, render_template
from sqlalchemy.orm.session import make_transient


bp_stats = Blueprint('stats', __name__, url_prefix='/stats')


@bp_stats.route('', methods=['GET', 'POST'])
def index():
    from main import db, config
    from app.models.task import BaseTask
    with db.session.no_autoflush:
        for task in config['tasks']:
            final_tasks = []
            tasks_db = BaseTask.query.filter_by(
                type=task['type']).order_by(BaseTask.date.desc()).all()
            for task_db in tasks_db:
                if task_db.date.strftime('%Y-%m-%d') not in [task.date.strftime('%Y-%m-%d') for task in final_tasks]:
                    local_task = BaseTask(type=task_db.type, date=task_db.date)
                    make_transient(task_db)
                    local_task.add(task_db)
                    final_tasks.append(
                        local_task)

                else:
                    local_task = [local_task for local_task in final_tasks if local_task.date.strftime(
                        '%Y-%m-%d') == task_db.date.strftime('%Y-%m-%d')][0]
                    local_task.add(task_db)
            for input in task['inputs']:
                input['datasets'] = []
                for local_task in final_tasks:

                    local_inputs = [
                        local_input for local_input in local_task.inputs if local_input.type == input['id']]
                    for local_input in local_inputs:
                        dict_inputs = local_input.to_dict()
                        for dict_input in dict_inputs:
                       
                            if dict_input['label'] not in [dataset['label'] for dataset in input['datasets']]:
                                input['datasets'].append({'label': dict_input['label'], 'data': [
                                                {'x':  local_task.date.strftime('%Y-%m-%d'), 'y': dict_input['value']}]})
                            else:
                                dataset_id = [
                                    i for i in range(0, len(input['datasets'])) if input['datasets'][i]['label'] == dict_input['label']][0]
                                input['datasets'][dataset_id]['data'].append({'x':  local_task.date.strftime(
                                    '%Y-%m-%d'), 'y': dict_input['value']})
                     



    return render_template('stats.html', data=config['tasks'])
