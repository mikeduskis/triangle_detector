import json

from werkzeug.wrappers import BaseResponse as Response


class BadRequest(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.code = 400
        self.message = msg


def extract_sides(request):
    if not request.is_json:
        raise BadRequest('Expected application/json content type')
    sides = request.get_json()
    if 'a' not in sides:
        raise BadRequest('Request lacks "a" side')
    if 'b' not in sides:
        raise BadRequest('Request lacks "b" side')
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
        response.status_code = 500
        response.headers['Content-type'] = 'text/plain'
        response.response = [str(e)]

    return response
