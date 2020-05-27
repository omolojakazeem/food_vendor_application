from rest_framework import serializers
from .models import Notification


class NotifySerializer(serializers.ModelSerializer):
    class Meta:
        model= Notification
        fields = '__all__'

