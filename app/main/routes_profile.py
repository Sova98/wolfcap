from app.main import bp
from flask import render_template
from app import login_manager
from app.models.user import User
from app.code import db_operations as db_ops
from app.config_db import db_config, db_use_class
from flask_login import login_required


@login_manager.user_loader
def load_user(user_id):
    req_user = db_ops.load_user_by_id(user_id=user_id, db_use_class=db_use_class, db_config=db_config)
    return req_user.result


@bp.route('/profile/<id>', methods=['POST', 'GET'])
@login_required
def profile(id):
    req_user = db_ops.load_user_by_id(user_id=id, db_use_class=db_use_class, db_config=db_config)
    if req_user.success:
        req_user_awards = db_ops.load_all_user_awards(user_id=req_user.result.id, db_use_class=db_use_class,db_config=db_config)
    return render_template('profile.html', user=req_user.result, awards=req_user_awards.result)