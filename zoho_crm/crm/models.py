from django.db import models

from base.base_models import BaseModel


class Lead(BaseModel):
    name = models.CharField(max_length=100, help_text="name of the lead")
    email = models.EmailField(help_text="email id")
    phone = models.CharField(
        max_length=20, null=True, blank=True, help_text="phone number"
    )

    def __str__(self):
        return self.name
