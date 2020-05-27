from django.db import models

from order.models import Order

from customer.models import Customer
from vendor.models import Vendor


class Notification(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_status = models.CharField(max_length=50)
    order = models.ForeignKey(Order,on_delete=models.CASCADE,)
    notification_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order} is currently {self.order_status}"
