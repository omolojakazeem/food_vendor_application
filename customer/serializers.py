from rest_framework import serializers

from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedIdentityField(many=False, view_name='account:user_detail')

    class Meta:
        model = Customer
        fields = '__all__'
