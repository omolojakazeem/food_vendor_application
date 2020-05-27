from rest_framework import serializers

from .models import Menu


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['name','description', 'price', 'menu_cat']


class MenuSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'
