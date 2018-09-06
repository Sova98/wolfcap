from app.main import bp
from flask import render_template
from app import login_manager
from app.models.user import User
from app.code import db_operations as db_ops
from app.config_db import db_config, db_use_class
import json
from flask import request
import app.code.json_utils as ju
from flask_login import login_required
from flask_login import current_user


@bp.route('/admin_awards_types', methods=['POST', 'GET'])
@login_required
def admin_awards_types():
    if current_user.is_admin == 0:
        return "Кыш"
    req_types = db_ops.load_all_task_tags(db_use_class=db_use_class, db_config=db_config)
    return render_template('admin_awards_type.html', awards_types=req_types.result)


@bp.route('/admin_awards', methods=['POST', 'GET'])
@login_required
def admin_awards():
    if current_user.is_admin == 0:
        return "Кыш"
    req_types = db_ops.load_all_task(db_use_class=db_use_class, db_config=db_config)
    return render_template('admin_awards.html', awards=req_types.result)


@bp.route('/add_award', methods=['POST'])
@login_required
def add_award():
    if current_user.is_admin == 0:
        return "Кыш"
    params = json.loads(request.data.decode('utf-8'))
    name = params['name']
    requirement = params['requirement']
    coins = params['coins']
    experience = params['experience']
    id_award_type = params['id_award_type']
    image_src = params['image_src']

    req_add_award = db_ops.create_award(name=name, requirement=requirement, coins=coins, experience=experience,
                                    id_award_type=id_award_type, image_src = image_src,db_use_class=db_use_class, db_config=db_config)

    if req_add_award.success:
        return ju.get_response_success(data=req_add_award.result)
    else:
        return ju.get_response_error(req_add_award.err_msg)



@bp.route('/delete_award', methods=['POST'])
@login_required
def delete_award():
    if current_user.is_admin == 0:
        return "Кыш"
    params = json.loads(request.data.decode('utf-8'))
    id_award = params['id_award']

    req_delete_award = db_ops.delete_award(id_award=id_award, db_use_class=db_use_class, db_config=db_config)

    if req_delete_award.success:
        return ju.get_response_success(data=req_delete_award.result)
    else:
        return ju.get_response_error(req_delete_award.err_msg)


@bp.route('/requests', methods=['POST', 'GET'])
@login_required
def requests():
    if current_user.is_admin == 0:
        return "Кыш"
    req_requests = db_ops.load_all_requests(db_use_class=db_use_class, db_config=db_config)

    return render_template('requests_awards.html', requests=req_requests.result)


@bp.route('/reward', methods=['POST', 'GET'])
@login_required
def reward():
    if current_user.is_admin == 0:
        return "Кыш"
    params = json.loads(request.data.decode('utf-8'))
    id_user = params['id_user']
    id_award = params['id_award']
    id_request = params['id_request']
    req_reward = db_ops.reward(id_user = id_user, id_award=id_award,
        id_request=id_request, db_use_class=db_use_class, db_config=db_config)
    if req_reward.success:
        return ju.get_response_success(data=req_reward.result)
    else:
        return ju.get_response_error(req_reward.err_msg)



@bp.route('/get_pg_equipment', methods=['POST', 'GET'])
def get_pg_equipment():
    req_equipment= db_ops.get_pg_equipment(db_use_class=db_use_class, db_config=db_config)
    if req_equipment.success:
        return 'подключился'
    else:
        return 'не подключился' + req_equipment.err_msg
