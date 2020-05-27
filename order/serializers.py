from rest_framework import serializers
from .models import Order, OrderMenu


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class OrderMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderMenu
        fields = ['menu','description']


class MyOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['customer','vendor','description','order_ref']


class OrderSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

        read_only_fields = ('customer', 'vendor', 'order_ref','description')


class OrderSerializer3(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_status']

        #read_only_fields = ('customer', 'vendor', 'order_ref','description')
