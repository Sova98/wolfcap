# -*- coding: utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False

    HOST = '127.0.0.1'
    PORT = 500

    IS_DEBUG = True
    #CERT = basedir + '/../555.cert'
    #KEY = basedir + '/../555.key'

    EXTERNAL_URL = 'https://127.0.0.1:555'

    # MAIL_SERVER = os.environ.get('MAIL_SERVER')
    # MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # ADMINS = ['your-email@example.com']

    # MAIL_SERVER = 'localhost'
    # MAIL_PORT = 8025
    # MAIL_USE_TLS = 0
    # MAIL_USERNAME = None #'android.telemaxima'
    # MAIL_PASSWORD = None #'yt/vfrcbv'
    # ADMINS = ['sannikov@telemaxima.ru']

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = 1
    MAIL_USERNAME = 'sovervos'
    MAIL_PASSWORD = 'perry_98'
    ADMINS = ['sovervos@gmail.com']

    DB_CONFIG = {'dbname': 'my_database', 'user': 'postgres', 'password': 'sovervo98', 'host': '127.0.0.1', 'port': '5432'}
