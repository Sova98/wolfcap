# -*- coding: utf-8 -*-
import os
from flask import Flask
from flask_login import LoginManager
import logging
from logging.handlers import RotatingFileHandler
from logging.handlers import SMTPHandler
from flask_mail import Mail

from app.config import Config

login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message = 'Зарегистрируйтесь для доступа к странице'

mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    login_manager.init_app(app)
    mail.init_app(app)

    #from app.auth import bp as auth_bp
    # app.register_blueprint(auth_bp, url_prefix='/auth')
    #app.register_blueprint(auth_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)


    if app.debug:
        if not os.path.exists('kapitan_logs'):
            os.mkdir('kapitan_logs')
        file_handler = RotatingFileHandler('kapitan_logs/kapitan.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('KAPITAN startup')



    if app.debug:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='ASCHOOL (error)',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

    return app


#Импорт моделей для синхронизации сруктуры БД модулем flask_migrate
# from app.models import  system_user, person, school, school_room
