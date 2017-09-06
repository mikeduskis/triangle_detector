import json
from unittest import TestCase, main, skip

from expects import expect, equal
import requests

from triangle_detector.server import Server

PORT = 4277


def build_request(**kwargs):
    return json.dumps({k: v for k, v in kwargs.items()})


class TestTransport(TestCase):

    def setUp(self):
        self.sut = Server()
        self.sut.start(port=PORT)

    def tearDown(self):
        self.sut.stop()

    def test_returns_status_200_on_valid_request_with_triangle(self):
        response = requests.post(
            'http://localhost:%d' % PORT,
            data=build_request(a=1, b=1, c=1))
        expect(response.status_code).to(equal(200))

    @skip('')
    def test_returns_status_200_on_valid_request_with_non_triangle(self):
        pass

    @skip('')
    def test_returns_content_type_json_on_valid_request(self):
        pass

    @skip('')
    def test_returns_json_payload_on_valid_request(self):
        pass

    @skip('')
    def test_returns_status_405_on_get(self):
        pass

    @skip('')
    def test_returns_status_400_on_no_payload(self):
        pass

    @skip('')
    def test_returns_status_400_on_non_json_payload(self):
        pass

    @skip('')
    def test_returns_status_400_on_missing_content_type(self):
        pass

    @skip('')
    def test_returns_status_400_on_wrong_content_type(self):
        pass

    @skip('')
    def test_returns_status_400_when_request_has_only_two_points(self):
        pass

    @skip('')
    def test_returns_status_400_when_request_lacks_a(self):
        pass

    @skip('')
    def test_returns_status_400_when_request_lacks_b(self):
        pass

    @skip('')
    def test_returns_status_400_when_request_lacks_c(self):
        pass

    @skip('')
    def test_returns_status_400_when_request_has_four_points(self):
        pass

    @skip('')
    def test_error_response_content_type_is_plain_text(self):
        pass


if '__main__' == __name__:
    main()
