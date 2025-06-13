import base64
import os
import uuid

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response


def generate_short_uuid():
    uid = uuid.uuid4()
    return base64.urlsafe_b64encode(uid.bytes).decode()[:12]


from rest_framework import status
from rest_framework.response import Response


def success_response(data, message="Success", status_code=200):
    return Response(
        {"status": True, "message": message, "data": data}, status=status_code
    )


def error_response(message="Error", status_code=400):
    return Response({"status": False, "message": message}, status=status_code)


def get_report_file_path(filename):
    reports_dir = os.path.join(settings.BASE_DIR, "media/reports/")
    os.makedirs(reports_dir, exist_ok=True)
    return os.path.join(reports_dir, filename)
