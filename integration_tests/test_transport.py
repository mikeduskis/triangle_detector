import json
from unittest import TestCase, main

from expects import expect, be_a, equal, have_length
import requests

from triangle_detector.server import Server

PORT = 4277
SERVICE_URL = 'http://localhost:%d' % PORT
JSON_HEADERS = {'Content-type': 'application/json'}


def send_request(content_type='application/json', **sides):
    headers = {}
    if content_type:
        headers['Content-type'] = content_type
    return requests.post(
        SERVICE_URL,
        headers=headers,
        data=json.dumps({k: v for k, v in sides.items()}))


class TestTransport(TestCase):

    def test_returns_status_200_on_valid_request_with_triangle(self):
        response = send_request(a=1, b=1, c=1)
        expect(response.status_code).to(equal(200))

    def test_returns_status_200_on_valid_request_with_non_triangle(self):
        response = send_request(a=1, b=1, c=3)
        expect(response.status_code).to(equal(200))

    def test_returns_content_type_json_on_valid_request(self):
        response = send_request(a=1, b=1, c=1)
        headers = response.headers
        assert 'Content-type' in headers
        expect(headers['Content-type']).to(equal('application/json'))

    def test_returns_json_list_with_exactly_one_bool_on_valid_request(self):
        response = send_request(a=1, b=1, c=1)
        try:
            returned = json.loads(response.text)
        except TypeError:
            assert False, 'Expected "%s" to be json' % response.text
        expect(returned).to(be_a(list))
        expect(returned).to(have_length(1))
        expect(returned[0]).to(be_a(bool))

    def test_returns_status_405_on_get(self):
        response = requests.get(SERVICE_URL)
        expect(response.status_code).to(equal(405))

    def test_returns_status_400_on_no_payload(self):
        response = requests.post(SERVICE_URL, headers=JSON_HEADERS)
        expect(response.status_code).to(equal(400))

    def test_returns_status_400_on_non_json_payload(self):
        response = requests.post(
            SERVICE_URL, headers=JSON_HEADERS, data='I am not Jason')
        expect(response.status_code).to(equal(400))

    def test_returns_status_400_on_missing_content_type(self):
        response = send_request(content_type=None, a=1, b=1, c=1)
        expect(response.status_code).to(equal(400))

    def test_returns_status_400_on_wrong_content_type(self):
        response = send_request(content_type='inedible/spam', a=1, b=1, c=1)
        expect(response.status_code).to(equal(400))

    def test_returns_status_400_when_request_has_only_two_points(self):
        response = send_request(a=1, c=1)
        expect(response.status_code).to(equal(400))

    def test_returns_status_400_when_request_lacks_a(self):
        response = send_request(b=1, c=1, n=1)
        expect(response.status_code).to(equal(400))

    def test_returns_status_400_when_request_lacks_b(self):
        response = send_request(a=1, c=1, n=1)
        expect(response.status_code).to(equal(400))

    def test_returns_status_400_when_request_lacks_c(self):
        response = send_request(a=1, b=1, n=1)
        expect(response.status_code).to(equal(400))

    def test_returns_status_400_when_request_has_four_points(self):
        response = send_request(a=1, b=1, c=1, n=1)
        expect(response.status_code).to(equal(400))

    def test_error_response_content_type_is_plain_text(self):
        response = send_request(a=1, b=1)
        expect(response.headers['Content-type']).to(equal('text/plain'))


if '__main__' == __name__:
    server = Server()
    server.start(port=PORT)
    try:
        main()
    finally:
        server.stop()
