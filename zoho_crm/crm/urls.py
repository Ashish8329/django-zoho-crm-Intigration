from django.urls import include, path

from . import views
from .views import create_lead_in_zoho, get_access_token

urlpatterns = [
    path("get-access-token/", views.get_access_token, name="get_access_token"),
    path("create-lead/", views.create_lead, name="create_lead"),
    path("get-lead/", views.get_lead, name="get_lead"),
    path("zoho-webhook/", views.zoho_webhook, name="zoho-webhook"),
]
