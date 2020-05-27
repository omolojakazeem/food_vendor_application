from django.urls import path

from .views import PaymentList, OrderPaymentView

urlpatterns = [
    path('', PaymentList.as_view(), name = 'order_payment_list'),
    path('<order_ref>/', OrderPaymentView.as_view(), name = 'order_payment'),

]