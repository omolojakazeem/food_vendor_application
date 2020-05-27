from django.db import models

from customer.models import Customer
from order.models import Order


class OrderPayment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    order_amount = models.FloatField()
    payment_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer.get_full_name
