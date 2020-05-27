from django.db import models

from vendor.models import Vendor

MENU_CAT = (
    ('main', 'Main'),
    ('side', 'Side')
)


class Menu(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    price = models.FloatField()
    quantity = models.IntegerField(default=1)
    menu_cat = models.CharField(choices=MENU_CAT, max_length=5)
    date_created = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)
    vendor_id = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    is_recurring = models.BooleanField(default=False)
    recurring_freq = models.IntegerField(default=1)

    def __str__(self):
        return self.name
