# -*- coding: utf-8 -*-
from flask import Blueprint

bp = Blueprint('main', __name__)

from app.main import routes_profile, routes_tasks, routes_rating, routes_auth, routes_admin_home, routes_news, routes_shop
