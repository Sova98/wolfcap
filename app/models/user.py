# -*- coding: utf-8 -*-

from time import time
import jwt
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.config_db import db_config, db_use_class
from app.config import Config
from app.models.web_object import WebObject

ROLE_USER = 0  # Обычный пользователь без привилегий
ROLE_ADMIN = 1  # Администратор


class User(UserMixin, WebObject):
    def __init__(self, id: int, name: str, login: str, password_hash: str,
                 login_confirmed: int, coins : int, experience : int, level : int, is_admin: int):
        self.id = id
        self.name = name
        self.login = login
        self.login_confirmed = login_confirmed
        self.coins = coins
        self.experience = experience
        self.level = level
        self.password_hash = password_hash
        self.authenticated = False
        self.is_admin = is_admin
        # доступные для пользователя справочники
        self.alowed_manuals = []
        self.alowed_domains = []
        self.roles = []

    def add_allowed_manual(self, id_manual: int):
        if id_manual not in self.alowed_manuals:
            self.alowed_manuals.append(id_manual)

    @property
    def is_authenticated(self):
        return self.login_confirmed == 1


    def __repr__(self):
        return '<Системный пользователь: {}>'.format(self.name)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def allowed_manual(self, id_manual: int) -> bool:
        return id_manual in self.alowed_manuals

    def allowed_role(self, id_role: int) -> bool:
        return id_role in self.roles

    def get_confirm_login_token(self, expires_in=600):
        return jwt.encode(
            {'confirm_password': self.id,
             'exp': time() + expires_in
             },
            Config.SECRET_KEY,
            algorithm='HS256'
        ).decode('utf-8')

    @staticmethod
    def verify_confirm_login_token(token):
        try:
            id = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])['confirm_password']
        except:
            return None

        from app.code import db_operations as db_ops
        res = db_ops.load_user_by_id(id, db_use_class, db_config)
        if res.success:
            return res.result
        else:
            return None


class SysUserUtils:
    def is_support_manual(user: User, id_manual: int) -> bool:
        if user and isinstance(user, User):
            return user.allowed_manual(id_manual)
        else:
            return False
