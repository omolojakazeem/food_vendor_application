from django.conf import settings
from django.db import models

# Create your models here.
from phone_field import PhoneField


class Vendor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    business_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = PhoneField(help_text='Vendor phone number')
    registered_on = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.business_name
