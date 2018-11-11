from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.menu_list, name='menu_list'),
    url(r'(?P<pk>\d+)/edit/$', views.edit_menu, name='edit_menu'),
    url(r'(?P<pk>\d+)/detail/$', views.menu_detail, name='menu_detail'),
    url(r'item/list/$', views.item_list, name='item_list'),
    url(r'item/(?P<pk>\d+)/$', views.item_detail, name='item_detail'),
    url(r'item/(?P<pk>\d+)/change/$', views.item_edit, name='item_edit'),
    url(r'new/$', views.create_new_menu, name='menu_new'),
]
