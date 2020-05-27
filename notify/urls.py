from django.urls import path

from .views import NotificationListView,NotificationDetail

urlpatterns = [
    path('', NotificationListView.as_view(), name = 'notify_list'),
    path('detail/<pk>',NotificationDetail.as_view(), name = 'notify_detail')
]