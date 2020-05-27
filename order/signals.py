from django.dispatch import Signal

new_order_notification = Signal(providing_args=["customer", "vendor","order","order_status",])

update_order_notification = Signal(providing_args=["order",])
