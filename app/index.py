import datetime
from flask import Blueprint, Flask, jsonify, request, flash, url_for, redirect, render_template

bp_index = Blueprint('index', __name__, url_prefix='/index')

@bp_index.route('', methods=['GET'])
def index():
    return render_template('index.html')



    
    

    
    
    

    
