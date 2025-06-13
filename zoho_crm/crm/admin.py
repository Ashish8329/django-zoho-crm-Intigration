from django.contrib import admin

from base.base_admin import BaseAdmin

from .models import Lead

# Register your models here.


@admin.register(Lead)
class LeadAdmin(BaseAdmin):
    list_display = ("name", "email", "phone")
