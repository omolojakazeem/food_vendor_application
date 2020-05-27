from django.db import models
from django.db import models
from vendor.models import Vendor
from customer.models import Customer

from menu.models import Menu

ORDER_STAT = (
    ('Initiated','Initiated'),
    ('On Queue', 'On Queue'),
    ('In Progress', 'In Progress'),
    ('Ready', 'Ready'),
    ('Cancelled', 'Cancelled')
)


class OrderMenu(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def get_menu_price(self):
        return self.menu.price * self.quantity

    def __str__(self):
        return f"{self.quantity} quantity of {self.menu.name} for {self.customer.get_full_name}"


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    description = models.TextField()
    order_ref = models.CharField(max_length=50)
    order_status = models.CharField(choices=ORDER_STAT, max_length=20, default="Initiated")
    order_items = models.ManyToManyField(OrderMenu)
    order_timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def get_total_order_price(self):
        total = 0
        for order_item in self.order_items.all():
            total += order_item.get_menu_price()
        return round(total,2)

    def __str__(self):
        return f"Customer = {self.customer.get_full_name} and Amount = {self.get_total_order_price}"






