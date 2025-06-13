from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Lead
from .urls import create_lead_in_zoho


@receiver(post_save, sender=Lead)
def process_zoho_lead_generation(sender, instance, created, **kwargs):
    """
    This will generate the lead on the zoho crm.
    """
    if created:
        result = create_lead_in_zoho(instance.name, instance.email, instance.phone)
        # print(result)
