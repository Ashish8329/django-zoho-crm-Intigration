# leads/views.py
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from base.utils import error_response, success_response
from zoho.leads import create_lead_in_zoho, process_access_token


@api_view(["POST"])
def get_access_token(request):
    """
    DRF View: Fetch access token from Zoho
    """
    try:
        token_data = process_access_token()
        return success_response(token_data)
    except Exception as e:
        return error_response(str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def create_lead(request):
    """
    DRF View: Create a lead in Zoho CRM.
    Expects JSON payload with 'name', 'email', 'phone'.
    """
    name = request.data.get("name")
    email = request.data.get("email")
    phone = request.data.get("phone")

    if not all([name, email, phone]):
        return error_response(
            "Missing name, email, or phone", status_code=status.HTTP_400_BAD_REQUEST
        )

    try:
        result = create_lead_in_zoho(name, email, phone)
        return success_response(result)
    except Exception as e:
        return error_response(str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
