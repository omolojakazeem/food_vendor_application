from django.conf.global_settings import EMAIL_HOST_USER
from django.core.mail import send_mail, send_mass_mail
from django.dispatch import receiver
from django.http import Http404

from order.signals import new_order_notification,update_order_notification

from .models import Notification
from .serializers import NotifySerializer


@receiver(new_order_notification)
def notify(sender, **kwargs):
    order_info = {
        'customer': kwargs['customer'],
        'vendor': kwargs['vendor'],
        'order_status': kwargs['order_status'],
        'order': kwargs['order'],
    }

    notification_serializer_data = NotifySerializer(data=order_info)
    if notification_serializer_data.is_valid(raise_exception=True):
        notification_saved = notification_serializer_data.save()
        vendor_email = notification_saved.order.vendor.email
        customer_email = notification_saved.order.customer.email
        message1 = f"Your Order {notification_saved.order}'s " \
                  f"has been received. Kindly make payment." \
                  f" Order status changed to " \
                  f"'{order_info['order_status']}'"
        message2 = f"Order {notification_saved.order}'s " \
                   f"has been Initiated." \
                   f" Order status changed to " \
                   f"'{order_info['order_status']}'"

        email_messages = (
            ('VGG FOOD VENDOR APP: Order Initiation', message1, EMAIL_HOST_USER, [customer_email]),
            ('VGG FOOD VENDOR APP: Order Initiation', message2, EMAIL_HOST_USER, [vendor_email]),
        )
        send_mass_mail(email_messages)


@receiver(update_order_notification)
def notify_update(sender, **kwargs):
    order = kwargs['order']
    notification = Notification.objects.get(order=order)

    order_info = {
        'customer': order.customer.pk,
        'vendor': order.vendor.pk,
        'order_status':order.order_status,
        'order': order.pk
    }

    notification_serializer_data = NotifySerializer(notification,data=order_info)
    if notification_serializer_data.is_valid(raise_exception=True):
        notification_serializer_data.save()
        message = f"Your Order {order}'s status has been changed to {order_info['order_status']}"
        vendor_email = order.vendor.email
        customer_email = order.customer.email
        print('Order Updated')
        send_mail(
            'VGG FOOD VENDOR APP: Email Confirmation',
            message,
            EMAIL_HOST_USER,
            [customer_email,vendor_email],
            fail_silently=False,
        )
