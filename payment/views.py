from customer.models import Customer
from django.http import Http404
from order.models import Order
from order.serializers import OrderSerializer3
from order.signals import update_order_notification

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import OrderPayment
from .serializers import OrderPaymentSerializer, OrderPaymentSerializer2


class PaymentList(APIView):

    def get(self, request, *args, **kwargs):
        payment = OrderPayment.objects.all()
        serializer = OrderPaymentSerializer2(payment, many=True)
        payment_data = serializer.data
        context = {
            'Payment': payment_data
        }
        return Response(context)

    def post(self, request, *args, **kwargs):
        payment_data = request.data
        serializer = OrderPaymentSerializer(data=payment_data)
        if serializer.is_valid(raise_exception=True):
            order = serializer.validated_data.get('order')
            order = Order.objects.get(pk=order.pk)
            order_amount = order.get_total_order_price
            customer = order.customer.email
            customer = Customer.objects.get(email=customer)

            order_payment_saved = serializer.save(
                order=order,
                customer=customer,
                order_amount=order_amount
                )
            the_order = {
                'order_status':"On Queue"
            }

            change_order_status = OrderSerializer3(order, data=the_order)
            if change_order_status.is_valid(raise_exception=True):
                order_update = change_order_status.save()
                update_order_notification.send(
                    sender=order_update,
                    order=order,
                )

            return Response({
                "Success": "You have successfully made Payment for the {} Order".format(order_payment_saved)
            })


class OrderPaymentView(APIView):

    def get_object(self, order_ref):
        try:
            order = Order.objects.get(order_ref=order_ref, )
            return order
        except Order.DoesNotExist:
            raise Http404

    def get(self, request, order_ref, *args, **kwargs):
        order_payment = self.get_object(order_ref)
        payment_serializer = OrderPaymentSerializer(order_ref, )
        return Response(payment_serializer.data, status=status.HTTP_200_OK)
