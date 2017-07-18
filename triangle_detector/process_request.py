from werkzeug.wrappers import BaseResponse as Response


def process_request(request, handler):

    return Response(
        status=404,
        response='There is nothing to see here.',
        content_tyep='text/plain')
