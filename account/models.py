from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db import models

# Create your models here.
USER_TYPE = (
    ("VENDOR", "VENDOR"),
    ("ADMIN", "ADMIN"),
    ("CUSTOMER", "CUSTOMER")
)


class User(AbstractUser):
    username = models.CharField(blank=True, null=True, max_length=50)
    email = models.EmailField(_('email address'), unique=True)
    user_type = models.CharField(max_length=15, choices=USER_TYPE, )

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return "{}".format(self.email)