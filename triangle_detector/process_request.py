import json

from werkzeug.wrappers import BaseResponse as Response


class BadRequest(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.code = 400
        self.message = msg


def extract_sides(request):
    sides = request.get_json()
    if len(sides) < 3:
        raise BadRequest('A triangle must have three sides')
    if 'a' not in sides:
        raise BadRequest('Request lacks "a" side')
    if 'c' not in sides:
        raise BadRequest('Request lacks "c" side')
    try:
        return {k: float(sides[k]) for k in ('a', 'b', 'c')}
    except ValueError as e:
        raise BadRequest('All sides must be numbers')


def process_request(request, handler):
    response = Response(
        status=200,
        content_type='application/json')

    try:
        sides = extract_sides(request)
        response.response = [json.dumps([handler(**sides)])]
    except BadRequest as e:
        response.status_code = e.code
        response.headers['Content-type'] = 'text/plain'
        response.response = [e.message]
    except Exception as e:
        # Preserve status codes from Werkzeug exceptions
        response.status_code = e.code if hasattr(e, 'code') else 500
        response.headers['Content-type'] = 'tin/spam'
        response.response = [str(e)]

    return response
