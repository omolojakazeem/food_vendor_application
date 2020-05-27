from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Notification
from .serializers import NotifySerializer


class NotificationListView(APIView):

    def get(self, request, *args, **kwargs):
        notification = Notification.objects.all()
        serializer = NotifySerializer(notification, many=True)
        notification_data = serializer.data
        context = {
            'Notifications': notification_data
        }
        return Response(context)


    def post(self, request, *args, **kwargs):
        notification_data = request.data
        serializer = NotifySerializer(data=notification_data)
        if serializer.is_valid(raise_exception=True):
            notification_data_save = serializer.save()
            return Response({
                "Success": "You have successfully created Notification for '{}' Order".format(notification_data_save.order)
            })


class NotificationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotifySerializer
    permission_classes = [AllowAny,]