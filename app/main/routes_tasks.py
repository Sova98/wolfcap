from app.main import bp
from flask import render_template, request
from app import login_manager
from app.models.user import User
from app.code import db_operations as db_ops
import json
from app.config_db import db_config, db_use_class
import app.code.json_utils as ju
from flask_login import login_required
from flask_login import current_user

@bp.route('/tasks', methods=['POST', 'GET'])
@login_required
def tasks():
    req_user = db_ops.load_user_by_id(current_user.id)
    return render_template('tasks.html')


@bp.route('/tasks/<id>', methods=['POST', 'GET'])
@login_required
def tasks_by_type(id):
    tasks = db_ops.load_all_task_by_category(category=id, db_use_class=db_use_class, db_config=db_config)
    return render_template('tasks_by_genre.html', tasks=tasks.result)


@bp.route('/get_all_task_tags', methods=['POST'])
@login_required
@ju.safe_execute_json
def get_all_task_tags(user : User= None):
    tasks = db_ops.load_all_task_tags(db_use_class=db_use_class, db_config=db_config)

    if tasks.success:
        return ju.get_response_success(data=ju.stringify(tasks.result))
    else:
        return ju.get_response_error(tasks.err_msg)


@bp.route('/add_request', methods=['POST'])
@login_required
@ju.safe_execute_json
def add_request():
    if current_user.is_admin == 0:
        return "Кыш"
    params = json.loads(request.data.decode('utf-8'))
    id_award = params['id_award']
    letter = params['letter']
    images = params['images']
    req_add_request = db_ops.add_award_request(id_user = current_user.id, id_award = id_award, letter = letter,
                                               images = images, db_use_class=db_use_class, db_config=db_config)

    if req_add_request.success:
        return ju.get_response_success(req_add_request.result)
    else:
        return ju.get_response_error(req_add_request.err_msg)