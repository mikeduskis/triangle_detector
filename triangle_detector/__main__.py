import sys

from flask import Flask, request

from .process_request import process_request
from .handlers import any_triangle, right_triangle, isosceles_triangle

service = Flask('test_result_archive')


@service.route('/', methods=['POST'])
def root():
    return process_request(request, handler=any_triangle)


@service.route('/right', methods=['POST'])
def right():
    return process_request(request, handler=right_triangle)


@service.route('/isosceles', methods=['POST'])
def isosceles():
    return process_request(request, handlder=isosceles_triangle)


if len(sys.argv) > 1:
    port = int(sys.argv[1])
else:
    port = 1333
service.run(host='0.0.0.0', port=port)
