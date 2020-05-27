from rest_framework import serializers

from .models import OrderPayment


class OrderPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPayment
        fields = ['order',]


class OrderPaymentSerializer2(serializers.ModelSerializer):
    class Meta:
        model = OrderPayment
        fields = '__all__'

