import base64
import uuid

from rest_framework import status
from rest_framework.response import Response
import os
from django.conf import settings


def generate_short_uuid():
    uid = uuid.uuid4()
    return base64.urlsafe_b64encode(uid.bytes).decode()[:12]


from rest_framework import status
from rest_framework.response import Response


def success_response(data=None, message="Success", request=None, extra_data={}):

    result = {
        "status": {"code": status.HTTP_200_OK, "message": message},
        "data": data,
    }

    result.update(extra_data)
    return Response(result)


def error_response(
    data=None,
    message="Error",
    status_code=None,
    request=None,
    code=status.HTTP_403_FORBIDDEN,
):
    if status_code:
        code = status_code
    return Response(
        {"status": {"code": code, "message": message}, "data": data}, status=code
    )


def get_report_file_path(filename):
    reports_dir = os.path.join(settings.BASE_DIR, "media/reports/")
    os.makedirs(reports_dir, exist_ok=True)
    return os.path.join(reports_dir, filename)