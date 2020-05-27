from django.urls import path

from .views import CustomerListViews, CustomerDetailView

urlpatterns = [
    path('', CustomerListViews.as_view(), name='customer_list'),
    path('detail/<pk>', CustomerDetailView.as_view(), name='customer_detail'),
]
