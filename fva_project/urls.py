
from rest_framework.documentation import include_docs_urls
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/customers/', include('customer.urls')),
    path('api/v1/vendors/', include('vendor.urls')),
    path('api/v1/orders/', include('order.urls')),
    path('api/v1/accounts/', include('account.urls')),
    path('api/v1/notifications/', include('notify.urls')),
    path('api/v1/menus/', include('menu.urls')),
    path('api/v1/payment/', include('payment.urls')),
    path('api/v1/', include('django.contrib.auth.urls')),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls))
    ]