from rest_framework import serializers

from .models import Vendor


class VendorSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedIdentityField(many=False, view_name='account:user_detail')

    class Meta:
        model = Vendor
        fields = '__all__'