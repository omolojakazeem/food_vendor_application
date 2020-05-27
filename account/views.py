from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.http import Http404
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserVerifySerializer, UserListSerializer
from .token import user_tokenizer


class LoginView(APIView):

    def get(self, request, *args, **kwargs):
        context = {
            "message": "Input your password"
        }
        return Response(context)

    def post(self, request, *args, **kwargs):

        my_user = request.data

        email = my_user.get('email')
        password = my_user.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            # request.session.save()
            context = {
                'Message': "Login Valid, welcome {}".format(request.user)
            }
            return Response(context)
        else:
            context = {
                'Message': "User invalid, Wrong credentials"
            }
            return Response(context)


class LogoutUser(APIView):

    def get(self, request, *args, **kwarg):
        context = {
            "Message": "Are you sure you want Logout?"
        }
        return Response(context)

    def post(self, request, *args, **kwarg):
        logout(request)
        context = {
            "Message": "'{}'Thank you, you have successfully logged out.".format(request.user)
        }
        return Response(context)


class UserList(APIView):


    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        serializer_context = {
            'request': request,
        }
        users_serializer = UserListSerializer(users, context=serializer_context, many=True)
        users_data = users_serializer.data
        context = {
            'Users': users_data,
        }
        return Response(users_data)


class UserDetail(APIView):

    def get_object(self, pk):
        try:
            user = User.objects.get(pk=pk)
            return user
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        user_serializer = UserListSerializer(user, many=False)
        user_data = user_serializer.data
        context = {
            'User': user_data,
        }
        return Response(context)

    def put(self, request, pk, *args, **kwargs):

        user = self.get_object(pk)
        user_serializer = UserListSerializer(user)
        if user_serializer.is_valid(raise_exception=True):
            user_serializer.save()
            context = {
                'user_data': user_serializer.data
            }
            return Response(context, )
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT'])
def activate_user(request, user_id, token, ):
    try:
        user_id = force_text(urlsafe_base64_decode(user_id))
        user = User.objects.get(pk=user_id)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and user_tokenizer.check_token(user, token):
        if request.method == 'GET':

            context = {
                "Message": "User Valid, Please set your Password"
            }
            return Response(context)

        elif request.method == 'PUT':
            my_user = UserVerifySerializer(user, data=request.data, partial=True)
            if my_user.is_valid(raise_exception=True):
                password = my_user.validated_data.get('password')
                password1 = request.data.get('password1')
                user = User.objects.get(pk=user_id)
                if password == password1:

                    user_password = make_password(password)
                    my_user.save(password=user_password, is_active=True)
                    context = {
                        "Message": "User Valid, Password Set Successfully"
                    }
                    return Response(context)
                else:
                    context = {
                        "Message": "Password Does Not match"
                    }
                    return Response(context)

    context = {
        "Message": "Invalid activation Link"
    }
    return Response(context)
