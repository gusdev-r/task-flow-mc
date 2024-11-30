from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request


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


def generate_hateoas_links(
    request: Request, resource_name: str, obj_id: int, request_type
) -> dict:
    base_url = request.build_absolute_uri(f"/{resource_name}/")
    links = {}

    if request_type == "get":
        links["self"] = f"{base_url}{obj_id}/"
        links["update"] = f"{base_url}{obj_id}/update/"
        links["delete"] = f"{base_url}{obj_id}/delete/"

    elif request_type == "post":
        links["self"] = f"{base_url}{obj_id}/"
        links["list"] = f"{base_url}"

    elif request_type == "put":
        links["self"] = f"{base_url}{obj_id}/"
        links["delete"] = f"{base_url}{obj_id}/delete/"

    elif request_type == "delete":
        links["self"] = f"{base_url}{obj_id}/"

    return links
