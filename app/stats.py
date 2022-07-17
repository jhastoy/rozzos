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
                print(task_db.inputs)
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
                    datasets = []
                    for local_input in local_inputs:
                        dict_inputs = local_input.to_dict()
                        for dict_input in dict_inputs:

                            if dict_input['label'] not in [dataset['label'] for dataset in datasets]:
                                datasets.append({'label': dict_input['label'], 'data': [
                                                {'x':  local_task.date.strftime('%Y-%m-%d'), 'y': dict_input['value']}]})
                            else:
                                dataset = [
                                    dataset for dataset in datasets if dataset['type'] == local_input.type][0]
                                dataset['data'].append({'x':  local_task.date.strftime(
                                    '%Y-%m-%d'), 'y': dict_input['value']})

                    input['datasets'] = datasets

        # if len(final_tasks) > 0:
        #     print(final_tasks[0].inputs)
        #task['data'] = [task.to_dict() for task in final_tasks]

    print(config['tasks'])
    return render_template('stats.html', data=config['tasks'])
