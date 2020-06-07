import logging
from typing import Union

from flask import jsonify


def success(result: Union[str, int, bool, dict, list]):
    return jsonify({
        'success': True,
        'result': result
    })


def success_deleted():
    return jsonify({
        'success': True
    }), 204


def bad_request(msg: Union[str, dict, list] = 'Bad request', code: int = 400):
    return jsonify({
        'success': False,
        'error': [{'code': code, 'message': msg}] if isinstance(msg, str) else msg
    }), code


def not_authorized(msg: Union[str, dict, list] = 'Not authorized'):
    return bad_request(msg, 401)


def forbidden(msg: Union[str, dict, list] = 'Forbidden'):
    return bad_request(msg, 403)


def not_found(msg: Union[str, dict, list] = 'Not found'):
    return bad_request(msg, 404)


def conflict(msg: Union[str, dict, list] = 'Conflict'):
    return bad_request(msg, 409)


def marshmallow_errors(errors):
    errors_list = []
    try:
        for key, value in errors.items():
            if isinstance(value, list):
                errors_list.append({
                    'code': key,
                    'message': ','.join(value)
                })
            elif isinstance(value, dict):
                for i, error_data_object in value.items():
                    if isinstance(error_data_object, list):
                        for err_text in error_data_object:
                            errors_list.append({
                                'code': '.'.join([str(key), str(i)]),
                                'message': err_text
                            })
                    elif isinstance(error_data_object, dict):
                        for fieldname, error_data in error_data_object.items():
                            errors_list.append({
                                'code': '.'.join([str(key), str(i), fieldname]),
                                'message': ','.join(error_data)
                            })
                    else:
                        errors_list.append({
                            'code': key,
                            'message': str(value)
                        })
            else:
                errors_list.append({
                   'code': key,
                   'message': str(value)
                })
    except Exception as exc:
        logging.exception(f'marshmallow_errors get exception - {exc}')

    return bad_request(errors_list, 400)
