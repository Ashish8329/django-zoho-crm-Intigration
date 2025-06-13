# leads/zoho.py
import os

import requests
from django.conf import settings


def process_access_token():
    """
    Obtain a new access token from Zoho using the refresh token.
    """
    url = f"{settings.ZOHO_API_BASE}/oauth/v2/token"

    data = {
        "refresh_token": settings.ZOHO_REFRESH_TOKEN,
        "client_id": settings.ZOHO_CLIENT_ID,
        "client_secret": settings.ZOHO_CLIENT_SECRET,
        "grant_type": "refresh_token",
    }
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()

        token_data = response.json()
        if "access_token" not in token_data:
            raise Exception(f"Access token not found in response: {token_data}")

        return token_data

    except requests.RequestException as e:
        raise Exception(f"Failed to fetch Zoho access token: {str(e)}")

    except Exception as e:
        raise Exception(f"Zoho token fetch failed: {str(e)}")


def create_lead_in_zoho(name, email, phone):
    """
    Creates a new lead in Zoho CRM using the access token.
    """
    try:
        token_data = process_access_token()
        access_token = token_data.get("access_token")
        if not access_token:
            raise Exception("Access token missing in response")

        url = f"{settings.ZOHO_API_BASE}/crm/v2/Leads"
        headers = {
            "Authorization": f"Zoho-oauthtoken {access_token}",
            "Content-Type": "application/json",
        }
        payload = {
            "data": [
                {
                    "Company": "Django Test",
                    "Last_Name": name,
                    "Email": email,
                    "Phone": phone,
                }
            ]
        }

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # raise for bad HTTP codes

        return response.json()

    except requests.RequestException as e:
        raise Exception(f"Error while creating lead in Zoho: {str(e)}")

    except Exception as e:
        raise Exception(f"Zoho lead creation failed: {str(e)}")
