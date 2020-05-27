from .views import activate_user,LoginView,LogoutUser, UserList, UserDetail
from django.urls import path, include

from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token

app_name = 'account'

urlpatterns = [
    path('user_reg/<user_id>/<token>', activate_user, name = 'auth_user_reg'),
    path('users_list/', UserList.as_view(), name = 'users_list'),
    path('user_detail/<pk>', UserDetail.as_view(), name = 'user_detail'),
    path('user_login/', LoginView.as_view(), name='auth_user_login'),
    path('user_logout/', LogoutUser.as_view(), name='auth_user_logout'),

    path('api-token-auth/', obtain_jwt_token),
    path('api-token-refresh/', refresh_jwt_token),
    path('api-token-verify/', verify_jwt_token),
    path('auth/', include('rest_auth.urls')),
]