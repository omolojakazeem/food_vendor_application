from account.serializers import UserCreateSerializer
from account.token import user_tokenizer

from django.core.mail import send_mail
from django.http import Http404
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from fva_project.settings import EMAIL_HOST_USER

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Customer
from .serializers import CustomerSerializer


class CustomerListViews(APIView):
    permission_classes = [AllowAny,]


    def get(self, request, *args, **kwargs):
        customers = Customer.objects.all()
        serializer_context = {
            'request': request,
        }
        ser_customers = CustomerSerializer(customers, context=serializer_context, many=True)
        customers_data = ser_customers.data
        context = {
            'Customers': customers_data,
        }
        return Response(context)


    def post(self, request, *args, **kwargs):
        new_customer = CustomerSerializer(data=request.data)
        if new_customer.is_valid(raise_exception=True):
            customer_email = new_customer.validated_data.get('email')
            cust = {
                'email': customer_email,
            }
            user = UserCreateSerializer(data=cust)
            if user.is_valid(raise_exception=True):
                new_user = user.save(is_active=False, user_type="CUSTOMER")
                new_customer_saved = new_customer.save(user=new_user, )

                user_id = urlsafe_base64_encode(force_bytes(new_user.pk))
                token = user_tokenizer.make_token(new_user)
                url = 'http://127.0.0.1:8000' + reverse('account:auth_user_reg', kwargs={'user_id': user_id, 'token': token})

                send_mail(
                    'VGG FOOD VENDOR APP: Email Confirmation',
                    url,
                    EMAIL_HOST_USER,
                    [customer_email],
                    fail_silently=False,
                )

                return Response({
                    'Success': "'{}' has been successfully registered".format(new_customer_saved.get_full_name)
                })

        return Response({
            'Failed': "Invalid information"
        })


class CustomerDetailView(APIView):

    def get_object(self, pk):
        try:
            customer = Customer.objects.get(pk=pk)
            return customer
        except Customer.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        customer = self.get_object(pk)
        cus_serializer = CustomerSerializer(customer, )
        return Response(cus_serializer.data)

    def put(self, request, pk, format=None):
        customer = self.get_object(pk)
        cus_serializer = CustomerSerializer(customer, data=request.data)
        if cus_serializer.is_valid():
            cus_serializer.save()
            return Response(cus_serializer.data)
        return Response(cus_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        customer = self.get_object(pk)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
