from datetime import datetime, timezone
from rest_framework.response import Response


def get_iso_now():
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def success_response(content=None, message="Success", status_code=200):
    payload = {
        "statusCode": status_code,
        "message": message,
        "content": content,
        "dateTime": get_iso_now(),
    }
    return Response(payload, status=status_code)


def raw_response(data, status_code=200):
    return Response(data, status=status_code)


def error_response(message="Error", status_code=400, content=None):
    payload = {
        "statusCode": status_code,
        "message": message,
        "content": content,
        "dateTime": get_iso_now(),
    }
    return Response(payload, status=status_code)

