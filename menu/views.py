from django.http import Http404
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from vendor.models import Vendor

from .models import Menu
from .serializers import MenuSerializer, MenuSerializer2


class MenuList(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer2
    permission_classes = [AllowAny, ]


class MenuDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer2
    permission_classes = [AllowAny, ]


class MenuListView(APIView):

    def get(self, request, *args, **kwargs):
        menu = Menu.objects.all()
        serializer = MenuSerializer2(menu, many=True)
        menu_data = serializer.data
        context = {
            'Menus': menu_data
        }
        return Response(context)

    def post(self, request, *args, **kwargs):
        menu_data = request.data
        serializer = MenuSerializer(data=menu_data)
        if serializer.is_valid(raise_exception=True):
            vendor = Vendor.objects.get(user=request.user)
            menu_data_save = serializer.save(vendor_id=vendor)
            return Response({
                "Success": "You have successfully created the {} Menu".format(menu_data_save.name)
            })


class MenuDetailView(APIView):
    permission_classes = [AllowAny]

    def get_object(self, pk):
        try:
            menu = Menu.objects.get(pk=pk, )
            return menu
        except Menu.DoesNotExist:
            raise Http404


    def get(self, request, pk, format=None):

        my_menu = self.get_object(pk=pk)
        menu_serializer = MenuSerializer2(my_menu, )
        return Response(menu_serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        my_menu = self.get_object(pk=pk)
        menu_serializer = MenuSerializer2(my_menu, )

        if menu_serializer.is_valid():
            menu_serializer.save()
            return Response(menu_serializer.data)
        return Response(menu_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        my_menu = self.get_object(pk=pk)
        my_menu.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
