from flask import render_template, request
from app import db
from app.modules.errors import module
# from app.api.errors import error_response as api_error_response

def wants_json_response():
    return request.accept_mimetypes['application/json'] >= \
        request.accept_mimetypes['text/html']

@module.app_errorhandler(404)
def not_found_error(error):
    if wants_json_response():
        # return api_error_response(404)
        pass
    return render_template('errors/404.html'), 404

@module.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    if wants_json_response():
        # return api_error_response(500)
        pass
    return render_template('errors/500.html'), 500