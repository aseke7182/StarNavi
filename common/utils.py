from rest_framework import status
from rest_framework.views import Response


def response(data, stat):
    return Response(data, status=stat)


def unauthorized(msg):
    return response({'detail': msg}, status.HTTP_401_UNAUTHORIZED)


def bad_request(msg):
    return response({'detail': msg}, status.HTTP_400_BAD_REQUEST)


def not_found(msg):
    return response({'detail': msg}, status.HTTP_404_NOT_FOUND)


def ok(data):
    if isinstance(data, str):
        data = {'detail': data}
    return response(data, status.HTTP_200_OK)


def created(data):
    return response(data, status.HTTP_201_CREATED)
