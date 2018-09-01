from app.main import bp
from flask import render_template, request, redirect, url_for
from app import login_manager
from app.models.user import User
import app.code.db_operations as db_ops
import json
from flask_bcrypt import generate_password_hash, check_password_hash
from app.config_db import db_config, db_use_class
import app.code.json_utils as ju
from flask_login import login_user
from flask_login import current_user
from app.config import Config
from app.mails import send_email


def send_login_confirmation_email(sys_user: User = None):
    token = sys_user.get_confirm_login_token()
    send_email('[ASchool] Confirm Your E-Mail',
               sender=Config.ADMINS[0],
               recipients=[sys_user.login],
               text_body=render_template('emails/confirm_email.txt',
                                         user=sys_user, token=token),
               html_body=render_template('emails/confirm_email.html',
                                         user=sys_user, token=token))


@bp.route('/confirm_email/<token>', methods=['GET', 'POST'])
@ju.safe_execute_json
def confirm_email(token):
    user = User.verify_confirm_login_token(token)
    if not user:
        return redirect(url_for('main.login'))

    user_verify = db_ops.system_user_update_properties(user.id, [('login_confirmed', 1)], db_use_class=db_use_class, db_config=db_config)
    if user_verify.success:
        login_user(user, remember=True)
        return redirect(url_for('main.profile', id=user.id))
    else:
        return ju.get_response_error(user_verify.err_msg)


@bp.route('/', methods=['POST', 'GET'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile', id=current_user.id))
    if request.method == 'POST':
        params = request.form
        email = params['user_email']
        password = params['user_password']
        name = params['username']
        password_hash = generate_password_hash(password).decode('utf-8')
        req_create_user = db_ops.create_user(name=name, email=email, password_hash=password_hash,
                                             db_use_class=db_use_class,
                                             db_config=db_config)
        if req_create_user.success:
            req_get_user = db_ops.load_user_by_login(email, db_use_class=db_use_class, db_config=db_config)
            if req_get_user.success:
                send_login_confirmation_email(req_get_user.result)
            return render_template('registration_success.html')
    return render_template('registration.html')


@bp.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile', id=current_user.id))
    if request.method == 'POST':
        params = request.form
        email = params['user_email']
        password = params['user_password']

        req_user = db_ops.load_user_by_login(login=email, db_use_class=db_use_class, db_config=db_config)

        if req_user.success:
            user_password_hash = req_user.result.password_hash
            if check_password_hash(user_password_hash, password):
                login_user(req_user.result, remember=True)
                return redirect(url_for('main.profile', id=req_user.result.id))
    return render_template('login.html')
