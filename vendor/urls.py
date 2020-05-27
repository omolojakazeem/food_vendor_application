from django.urls import path

from .views import VendorListView,VendorDetailView, VendorMenuListView

urlpatterns = [
    path('', VendorListView.as_view(), name='vendor_list'),
    path('detail/<pk>', VendorDetailView.as_view(), name='vendor_detail'),
    path('my_menu/<user>', VendorMenuListView.as_view(), name='vendor_menu'),

]
