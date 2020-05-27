from django.conf import settings
from django.db import models

# Create your models here.
from phone_field import PhoneField


class Customer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = PhoneField()
    registered_on = models.DateTimeField(auto_now_add=True)
    amount_outstanding = models.FloatField(default=0.0)
    last_updated = models.DateTimeField(auto_now=True)

    @property
    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return f"{self.get_full_name}({self.user.email})"

