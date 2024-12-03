from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from django.urls import reverse
from django.http import HttpRequest
from rest_framework.views import APIView


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
    request: HttpRequest,
    resource_name: str = None,
    obj_id: str = None,
    request_type: str = None,
) -> dict:
    base_url = request.build_absolute_uri(reverse(f"{resource_name}-list"))
    create_uri = request.build_absolute_uri(reverse(f"{resource_name}-create"))
    delete_uri = request.build_absolute_uri(
        reverse(f"{resource_name}-delete", args=[obj_id])
    )
    update_uri = request.build_absolute_uri(
        reverse(f"{resource_name}-update", args=[obj_id])
    )
    detail_uri = request.build_absolute_uri(
        reverse(f"{resource_name}-detail", args=[obj_id])
    )

    links = {}

    if request_type == "get" and obj_id:
        links["self"] = detail_uri
        links["search_all"] = base_url
        links["update"] = update_uri
        links["delete"] = delete_uri
        links["create"] = create_uri

    elif request_type == "get":
        links["self"] = base_url
        links["create"] = create_uri

    elif request_type == "post":
        links["self"] = create_uri
        links["update"] = update_uri
        links["search"] = detail_uri
        links["list"] = base_url

    elif request_type == "put":
        links["self"] = update_uri
        links["search"] = detail_uri
        links["search_all"] = base_url
        links["delete"] = delete_uri

    elif request_type == "delete":
        links["self"] = delete_uri
        links["search_all"] = base_url

    return links
