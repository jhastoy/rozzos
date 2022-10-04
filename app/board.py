from calendar import month
from copy import deepcopy
import datetime
import json
from flask import Blueprint, Flask, jsonify, request, flash, url_for, redirect, render_template
from sqlalchemy import false
from sqlalchemy.orm.session import make_transient
import calendar


bp_board = Blueprint('board', __name__, url_prefix='/board')


@bp_board.route('/<date1>_<date2>', methods=['GET', 'POST'])
def index(date1, date2):
    
    from main import db, config
    from app.models.task import BaseTask
    from app.models.inputs import Weighing


    with db.session.no_autoflush:
        for task in config['tasks']:
            
            tasks_db = BaseTask.query.filter(
                BaseTask.date.between(date1, date2)).filter_by(
                type=task['type']).all()
                
            total_task = BaseTask(type=task['type'])
            for task_db in tasks_db:
                total_task.add(task_db, period=True)
            task['data'] = total_task.to_dict(period=True)['data']
            for input in task['inputs']:
                input_match = [input_db.to_dict()
                                 for input_db in total_task.inputs if input_db.type == input['id']]
                if len(input_match) > 0:
                    input['data'] = input_match[0]
                
            
    # print(config['tasks'])
    return render_template('board.html', data=config['tasks'], date1=date1, date2=date2)


@bp_board.route('/day/<date1>_<date2>', methods=['GET', 'POST'])
def index_day(date1, date2):

    date1_prev = datetime.datetime.strptime(
        date1, '%Y-%m-%d') - datetime.timedelta(days=1)
    date1_prev = date1_prev.strftime('%Y-%m-%d')
    date2_prev = datetime.datetime.strptime(
        date2,  '%Y-%m-%d') - datetime.timedelta(days=1)
    date2_prev = date2_prev.strftime('%Y-%m-%d')

    date1_next = datetime.datetime.strptime(
        date1,  '%Y-%m-%d') + datetime.timedelta(days=1)
    date1_next = date1_next.strftime('%Y-%m-%d')

    date2_next = datetime.datetime.strptime(
        date2,  '%Y-%m-%d') + datetime.timedelta(days=1)
    date2_next = date2_next.strftime('%Y-%m-%d')

    config = get_data(date1, date2)
    
    return render_template('board.html', url="board.index_day",  date1=date1, date2=date2, data=config['tasks'], date1_prev=date1_prev, date2_prev=date2_prev,  date1_next=date1_next, date2_next=date2_next)


@bp_board.route('/day', methods=['GET', 'POST'])
def home_day():
    
    date1 = datetime.datetime.now()
    date2 = datetime.datetime.now() + datetime.timedelta(1)
    
    return redirect(url_for('board.index_day', date1=date1.strftime('%Y-%m-%d'), date2=date2.strftime('%Y-%m-%d')))
    
    
@bp_board.route('/week/<date1>_<date2>', methods=['GET', 'POST'])
def index_week(date1, date2):

    date1_prev = datetime.datetime.strptime(
        date1, '%Y-%m-%d') - datetime.timedelta(days=7)
    date1_prev = date1_prev.strftime('%Y-%m-%d')
    date2_prev = datetime.datetime.strptime(
        date2,  '%Y-%m-%d') - datetime.timedelta(days=7)
    date2_prev = date2_prev.strftime('%Y-%m-%d')

    date1_next = datetime.datetime.strptime(
        date1,  '%Y-%m-%d') + datetime.timedelta(days=7)
    date1_next = date1_next.strftime('%Y-%m-%d')

    date2_next = datetime.datetime.strptime(
        date2,  '%Y-%m-%d') + datetime.timedelta(days=7)
    date2_next = date2_next.strftime('%Y-%m-%d')

    config = get_data(date1, date2)

    return render_template('board.html', url="board.index_week",  date1=date1, date2=date2, data=config['tasks'], date1_prev=date1_prev, date2_prev=date2_prev,  date1_next=date1_next, date2_next=date2_next)


@bp_board.route('/week', methods=['GET', 'POST'])
def home_week():

    dt = datetime.datetime.now()

    date1 = dt - datetime.timedelta(days=dt.weekday())

    date2 = date1 + datetime.timedelta(days=6)

    
    return redirect(url_for('board.index_week', date1=date1.strftime('%Y-%m-%d'), date2=date2.strftime('%Y-%m-%d')))



@bp_board.route('/month/<date1>_<date2>', methods=['GET', 'POST'])
def index_month(date1, date2):

    days_month_prev_1 = calendar.monthrange(datetime.datetime.strptime(
        date1, '%Y-%m-%d').year, datetime.datetime.strptime(
        date1, '%Y-%m-%d').month - 1 if datetime.datetime.strptime(
        date1, '%Y-%m-%d').month - 1 != 0 else 12)[1]
    days_month_prev_2 = calendar.monthrange(datetime.datetime.strptime(
        date1, '%Y-%m-%d').year, datetime.datetime.strptime(
        date1, '%Y-%m-%d').month)[1]
    
    
    days_month_next_1 = calendar.monthrange(datetime.datetime.strptime(
        date1, '%Y-%m-%d').year, datetime.datetime.strptime(
        date1, '%Y-%m-%d').month + 1 if datetime.datetime.strptime(
        date1, '%Y-%m-%d').month + 1 != 13 else 1)[1]
    days_month_next_2 = calendar.monthrange(datetime.datetime.strptime(
        date1, '%Y-%m-%d').year, datetime.datetime.strptime(
        date1, '%Y-%m-%d').month)[1]
    
    date1_prev = datetime.datetime.strptime(
        date1, '%Y-%m-%d') - datetime.timedelta(days=days_month_prev_1)
    date1_prev = date1_prev.strftime('%Y-%m-%d')
    date2_prev = datetime.datetime.strptime(
        date2,  '%Y-%m-%d') - datetime.timedelta(days=days_month_prev_2)
    date2_prev = date2_prev.strftime('%Y-%m-%d')

    date1_next = datetime.datetime.strptime(
        date1,  '%Y-%m-%d') + datetime.timedelta(days=days_month_next_2)
    date1_next = date1_next.strftime('%Y-%m-%d')

    date2_next = datetime.datetime.strptime(
        date2,  '%Y-%m-%d') + datetime.timedelta(days=days_month_next_1)
    date2_next = date2_next.strftime('%Y-%m-%d')

    config = get_data(date1, date2)

    return render_template('board.html', url="board.index_month", data=config['tasks'], date1=date1, date2=date2, date1_prev=date1_prev, date2_prev=date2_prev,  date1_next=date1_next, date2_next=date2_next)


@bp_board.route('/month', methods=['GET', 'POST'])
def home_month():

    dt = datetime.datetime.now()


    days_month = calendar.monthrange(dt.year, dt.month)[1]
    date1 = datetime.datetime(dt.year, dt.month, 1)

    date2 = date1 + datetime.timedelta(days=days_month-1)

    return redirect(url_for('board.index_month', date1=date1.strftime('%Y-%m-%d'), date2=date2.strftime('%Y-%m-%d')))

def get_data(date1, date2):

    from main import db, config
    from app.models.task import BaseTask
    from app.models.inputs import Weighing
    config = deepcopy(config)
    
    with db.session.no_autoflush:
        for task in config['tasks']:

            tasks_db = BaseTask.query.filter(
                BaseTask.date.between(date1, date2)).filter_by(
                type=task['type']).all()

            total_task = BaseTask(type=task['type'])
            for task_db in tasks_db:
                total_task.add(task_db, period=True)
            task['data'] = total_task.to_dict(period=True)['data']
            for input in task['inputs']:
                input_match = [input_db.to_dict()
                               for input_db in total_task.inputs if input_db.type == input['id']]
                if len(input_match) > 0:
                    input['data'] = input_match[0]
    return config
