import random
import string

from customer.models import Customer
from django.http import Http404

from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order, OrderMenu
from .serializers import (
    OrderMenuSerializer,
    OrderSerializer,
    OrderSerializer2,
    MyOrderSerializer
)
from .signals import new_order_notification, update_order_notification
from menu.models import Menu


def get_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


class OrderListView(APIView):

    def get(self, request, *args, **kwargs):
        order = Order.objects.all()
        serializer_context = {
            'request':request,
        }

        serializer = OrderSerializer(order, context=serializer_context, many=True)
        order_data = serializer.data
        context = {
            'Orders': order_data
        }
        return Response(context)

    def post(self, request, *args, **kwargs):
        order_menu_request_data = request.data
        order_menu_serializer = OrderMenuSerializer(data=order_menu_request_data, )
        if order_menu_serializer.is_valid(raise_exception=True):

            menu_id = order_menu_serializer.validated_data.get('menu')
            description = order_menu_serializer.validated_data.get('description')

            menu = Menu.objects.get(pk=menu_id.pk)
            vendor = menu.vendor_id
            customer = Customer.objects.get(user=request.user)

            order_menu_saved = order_menu_serializer.save(
                vendor=vendor,
                customer=customer,
                menu=menu, )

            if order_menu_saved:
                ref_code = get_ref_code()
                order_context = {
                    'customer': customer.pk,
                    'vendor': vendor.pk,
                    'description': description,
                    'order_ref': ref_code,
                }

                order_request_data = MyOrderSerializer(data=order_context, )
                if order_request_data.is_valid(raise_exception=True):
                    order_saved = order_request_data.save()
                    order_saved.order_items.add(order_menu_saved)

                    new_order_notification.send(
                        sender=order_saved,
                        customer=order_saved.customer.pk,
                        vendor=order_saved.vendor.pk,
                        order=order_saved.pk,
                        order_status=order_saved.order_status
                    )

                    context = {
                        'New Order': order_saved,
                    }
                    return Response(context)
                context = {
                    'Message': "Invalid Inputs",
                }
                return Response(context)
            context = {
                'Message': "Invalid Inputs",
            }
            return Response(context)


class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny, ]


class OrderDetailView(APIView):
    permission_classes = [AllowAny, ]

    def get_object(self, pk):
        try:
            order = Order.objects.get(pk=pk)
            return order
        except Order.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        my_order = self.get_object(pk)
        order_serializer = OrderSerializer(my_order, many=False)
        return Response(order_serializer.data)

    def put(self, request, pk, format=None):
        order_data = request.data
        my_order = self.get_object(pk)
        order_serializer = OrderSerializer2(my_order, data=order_data)

        if order_serializer.is_valid():
            order = order_serializer.save()
            update_order_notification.send(
                sender=order,
                order=order,
            )
            return Response(order_serializer.data)
        return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        my_order = self.get_object(pk)
        my_order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderItemDetail(generics.RetrieveUpdateAPIView):
    queryset = OrderMenu.objects.all()
    serializer_class = OrderMenuSerializer
    permission_classes = [AllowAny, ]