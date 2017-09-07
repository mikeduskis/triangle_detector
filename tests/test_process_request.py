import json
from unittest import TestCase, main

from expects import expect, be_a, be, contain, equal
from werkzeug.wrappers import BaseResponse as Response


from triangle_detector.process_request import BadRequest, process_request


class FakeRequest:
    """
    Fakes Flask request
    http://flask.pocoo.org/docs/0.12/api/
    """

    def __init__(self, a=1, b=2, c=3, is_json=True):
        self.sides = {'a': a, 'b': b, 'c': c}
        self.is_json = is_json

    def get_json(self, *args, **kawrgs):
        return self.sides


class HandlerSpy:

    def __init__(self):
        self.a = None
        self.b = None
        self.c = None

    def __call__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        return True


class TestProcessRequest(TestCase):

    def test_response_is_a_response(self):
        response = process_request(FakeRequest(), lambda a, b, c: True)
        expect(response).to(be_a(Response))

    def test_response_response_is_a_list(self):
        response = process_request(FakeRequest(), lambda a, b, c: True)
        expect(response.response).to(be_a(list))

    def test_passes_a_from_request_to_handler_as_int(self):
        expected = 42
        request = FakeRequest(a=expected)
        spy = HandlerSpy()
        process_request(request, spy)
        expect(spy.a).to(equal(expected))

    def test_passes_b_from_request_to_handler_as_int(self):
        expected = 43
        request = FakeRequest(a=42, b=expected, c=99)
        spy = HandlerSpy()
        process_request(request, spy)
        expect(spy.b).to(equal(expected))

    def test_passes_c_from_request_to_handler_as_int(self):
        expected = 87
        request = FakeRequest(a=42, b=102, c=expected)
        spy = HandlerSpy()
        process_request(request, spy)
        expect(spy.c).to(equal(expected))

    def test_response_status_is_400_when_request_is_not_json(self):
        response = process_request(
            FakeRequest(is_json=False), lambda a, b, c: True)
        expect(response.status_code).to(equal(400))

    def test_response_status_is_400_when_request_lacks_a(self):
        request = FakeRequest()
        request.sides = {'b': 1, 'c': 2}
        response = process_request(request, lambda a, b, c: True)
        expect(response.status_code).to(equal(400))

    def test_response_status_is_400_when_request_lacks_b(self):
        request = FakeRequest()
        request.sides = {'a': 1, 'c': 2}
        response = process_request(request, lambda a, b, c: True)
        expect(response.status_code).to(equal(400))

    def test_response_status_is_400_when_request_lacks_c(self):
        request = FakeRequest()
        request.sides = {'a': 1, 'b': 2}
        response = process_request(request, lambda a, b, c: True)
        expect(response.status_code).to(equal(400))

    def test_response_status_is_400_when_request_has_four_sides(self):
        request = FakeRequest()
        request.sides = {'a': 1, 'b': 1, 'c': 1, 'd': 1}
        response = process_request(request, lambda a, b, c: True)
        expect(response.status_code).to(equal(400))

    def test_response_status_is_400_when_request_a_is_not_a_number(self):
        request = FakeRequest()
        request.sides = {'a': 'a', 'b': 2, 'c': 3}
        response = process_request(request, lambda a, b, c: True)
        expect(response.status_code).to(equal(400))

    def test_response_status_is_400_when_request_b_is_not_a_number(self):
        request = FakeRequest()
        request.sides = {'a': 1, 'b': 'two', 'c': 3}
        response = process_request(request, lambda a, b, c: True)
        expect(response.status_code).to(equal(400))

    def test_response_status_is_400_when_request_c_is_not_a_number(self):
        request = FakeRequest()
        request.sides = {'a': 1, 'b': 2, 'c': 'the spinach imposition'}
        response = process_request(request, lambda a, b, c: True)
        expect(response.status_code).to(equal(400))

    def tet_400_response_content_type_is_plain_text(self):
        def handler(a, b, c):
            raise BadRequest('whatever')
        request = FakeRequest()
        request.sides = {'a': 1, 'b': 1, 'c': 1}
        response = process_request(request, handler)
        expect(response.headers['Content-type']).to(equal('text/plain'))

    def test_response_has_json_content_type(self):
        response = process_request(FakeRequest(), lambda a, b, c: True)
        expect(response.headers['Content-type']).to(equal('application/json'))

    @staticmethod
    def extract_json(response):
        try:
            payload = response.response[0]
            return json.loads(payload)[0]
        except Exception as e:
            raise Exception(
                'Failed to decode response %s "%s" (%s: %s)'
                % (
                    type(response.response),
                    response.response, type(e), e)) from e

    def test_response_is_json_true_when_handler_returns_true(self):
        response = process_request(FakeRequest(), lambda a, b, c: True)
        expect(self.extract_json(response)).to(be(True))

    def test_reponse_status_is_200_when_handler_returns_true(self):
        response = process_request(FakeRequest(), lambda a, b, c: True)
        expect(response.status_code).to(equal(200))

    def test_response_is_json_false_when_handler_returns_false(self):
        response = process_request(FakeRequest(), lambda a, b, c: False)
        expect(self.extract_json(response)).to(be(False))

    def test_response_status_is_200_when_handler_returns_false(self):
        response = process_request(FakeRequest(), lambda a, b, c: False)
        expect(response.status_code).to(equal(200))

    def test_response_has_text_content_type_when_handler_raises_exception(self):
        def handler(a, b, c):
            raise Exception('intentional')

        response = process_request(FakeRequest(), handler)
        expect(response.headers['Content-type']).to(equal('text/plain'))

    def test_response_status_is_500_when_handler_raises_exception(self):
        def handler(a, b, c):
            raise Exception('intentional')

        response = process_request(FakeRequest(), handler)
        expect(response.status_code).to(equal(500))

    def test_uses_status_code_in_handler_exception(self):
        expected = 418

        def handler(a, b, c):
            e = Exception('I am a teapot')
            e.code = expected
            raise e

        response = process_request(FakeRequest(), handler)
        expect(response.status_code).to(equal(expected))

    def test_response_contains_exception_raised_by_handler(self):
        expected = "It's a fair cop."

        def handler(a, b, c):
            raise Exception(expected)
        response = process_request(FakeRequest(), handler)
        expect(response.response).to(contain(expected))


if '__main__' == __name__:
    main()
