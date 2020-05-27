from django.urls import path

from .views import MenuList, MenuDetail

urlpatterns = [
    path('',MenuList.as_view(),name = 'menu_list'),
    #path('menus/',MenuListView.as_view(),name = 'menu_list'),
    #path('menus/detail/<pk>',MenuDetailView.as_view(),name = 'menu_detail'),
    path('detail/<pk>',MenuDetail.as_view(),name = 'menu_detail'),

]
