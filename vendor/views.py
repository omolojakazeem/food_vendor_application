
from django.core.mail import send_mail
from django.http import Http404

from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Vendor
from .serializers import VendorSerializer

from account.models import User
from account.serializers import UserCreateSerializer
from account.token import user_tokenizer

from fva_project.settings import EMAIL_HOST_USER

from menu.models import Menu


class VendorListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):

        vendors = Vendor.objects.all()
        serializer_context = {
            'request': request,
        }
        ser_vendors = VendorSerializer(vendors, context=serializer_context, many=True)
        vendors_data = ser_vendors.data
        context = {
            'Vendors': vendors_data,
        }

        return Response(context)

    def post(self, request, *args, **kwargs):
        new_vendor = VendorSerializer(data=request.data)
        if new_vendor.is_valid(raise_exception=True):
            vendor_email = new_vendor.validated_data.get('email')
            vend = {
                'email': vendor_email,
            }
            user = UserCreateSerializer(data=vend)
            if user.is_valid(raise_exception=True):
                new_user = user.save(is_active=False, user_type="VENDOR")
                new_vendor_saved = new_vendor.save(user=new_user, )

                user_id = urlsafe_base64_encode(force_bytes(new_user.pk))
                token = user_tokenizer.make_token(new_user)
                url = 'http://127.0.0.1:8000' + reverse('account:auth_user_reg', kwargs={'user_id': user_id, 'token': token})

                send_mail(
                    'VGG FOOD VENDOR APP: Email Confirmation',
                    url,
                    EMAIL_HOST_USER,
                    [vendor_email],
                    fail_silently=False,
                )
                return Response({
                    'Success': "'{}' has been successfully registered".format(new_vendor_saved.business_name)
                })

        return Response({
            'Failed': "Invalid information"
        })


class VendorDetailView(APIView):

    def get_object(self, pk):
        try:
            vendor = Vendor.objects.get(pk=pk)
            return vendor
        except Vendor.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        vendor = self.get_object(pk)
        ven_serializer = VendorSerializer(vendor, )
        return Response(ven_serializer.data)

    def put(self, request, pk, format=None):
        vendor = self.get_object(pk)
        ven_serializer = VendorSerializer(vendor, data=request.data)
        if ven_serializer.is_valid():
            ven_serializer.save()
            return Response(ven_serializer.data)
        return Response(ven_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        vendor = self.get_object(pk)
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VendorMenuListView(APIView):

    def get(self, request, *args, **kwargs):
        vendor = User.objects.get(user=self.request.user)
        menus = Menu.objects.filter(vendor_id=vendor)
        ser_menus = VendorSerializer(menus, many=True)
        menu_data = ser_menus.data
        context = {
            'My Menus': menu_data,
        }

        return Response(context)
