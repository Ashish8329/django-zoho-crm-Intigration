# leads/views.py
import json

import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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


@api_view(["GET"])
def get_lead(request):
    """
    DRF View: Fetch leads from Zoho CRM with optional fields.
    Example: /api/get-lead/?fields=Email,Phone
    """
    fields = request.query_params.get("fields", "")

    try:
        token_data = process_access_token()
        access_token = token_data.get("access_token")
        if not access_token:
            return error_response(
                "Access token not found",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        url = f"https://www.zohoapis.in/crm/v2/Leads"
        headers = {"Authorization": f"Zoho-oauthtoken {access_token}"}
        params = {}

        if fields:
            params["fields"] = fields
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return success_response(response.json())
        else:
            return error_response(
                "Failed to fetch leads", status_code=response.status_code
            )

    except Exception as e:
        return error_response(str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
def zoho_webhook(request):
    if request.method == "POST":
        try:
            body_unicode = request.body.decode("utf-8")
            if not body_unicode:
                return JsonResponse({"error": "Empty payload"}, status=400)

            data = json.loads(body_unicode)

            # Process the event here TODO
            return JsonResponse({"message": "Webhook received"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Invalid method"}, status=405)
