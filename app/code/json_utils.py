# -*- coding: utf-8 -*-
import traceback


import json
from functools import wraps
from datetime import datetime
from decimal import Decimal

import app.code.exception_utils as exc_utils

from flask import jsonify


def safe_execute_json(func):
    """
    Декоратор для функций, которые должны результат возвращать в виде json
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as err:
            traceback.print_exc()
            return get_response_error(exc_utils.traceback_to_str(err))

    return wrapper


def serialize(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    elif isinstance(obj, Decimal):
        serial = float(obj)
        return serial

    # if isinstance(obj, time):
    #     serial = obj.isoformat()
    #     return serial

    return obj.__dict__


def stringify(obj) ->  str:
    return json.dumps(obj, default=serialize)


def get_response(data: str, url: str, status: str, msg: str) -> str:
    result = {"result": status};

    if url:
        result['url'] = url

    if data:
        result['data'] = data

    if msg:
        result['msg'] = msg

    return jsonify(result)


def get_response_success(data: str = '', url: str = '', msg: str = '') -> str:
    return get_response(data, url, 'OK', msg)


def get_response_error(msg: str = '') -> str:
    return get_response('', '', 'ERROR', msg)


def get_response_error__wrong_request() -> str:
    return get_response_error('Неправльная структура запроса');


def get_response_error__wrong_request_param(param_name: str, param_value, expected_value=None) -> str:
    if expected_value:
        return get_response_error("Неожиданное значение параметра '{}': {}. Ожидается: {}".format(param_name, param_value, expected_value))
    else:
        return get_response_error("Неожиданное значение параметра '{}': {}".format(param_name, param_value))