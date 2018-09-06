from app.main import bp
from flask import render_template
from app import login_manager
from app.models.user import User
from flask_login import login_required
import app.code.db_operations as db_ops
from app.config_db import db_config, db_use_class


@bp.route('/rating', methods=['POST', 'GET'])
@login_required
def rating():
    req_best_users = db_ops.load_best_users(db_use_class=db_use_class, db_config=db_config);
    return render_template('rating.html',
                            title='Рейтинг',
                            best_users=req_best_users.result)
