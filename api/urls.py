from django.contrib import admin
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

user_list = views.UserViewSet.as_view({
    'get': 'list'
})

user_detail = views.UserViewSet.as_view({
    'get': 'retrieve'
})

session_list = views.SessionViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

session_detail = views.SessionViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

track_detail = views.TrackViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


urlpatterns = format_suffix_patterns([
    url(r'^users/$', user_list, name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail'),
    url(r'^sessions/$', session_list, name='session-list'),
    url(r'^sessions/(?P<uuid>[0-9a-f-]+)/$', session_detail, name='session-detail'),
    url(r'^sessions/(?P<uuid>[0-9a-f-]+)/$', session_detail, name='session-detail'),
    url(r'^tracks/(?P<uuid>[0-9a-f-]+)/$', track_detail, name='track-detail'),


    url(r'^$', views.api_root)

])
