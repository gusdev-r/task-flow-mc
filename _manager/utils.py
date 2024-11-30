from rest_framework.response import Response
from rest_framework import status


def response_app(data, status_code=200, exception=False, obj=None, links=None):
    response_data = {
        "status_code": status_code,
        "exception": exception,
        "message": data,
    }
    if obj:
        response_data["data"] = obj
    if links is not None:
        response_data["links"] = links
    return Response(response_data, status_code)
