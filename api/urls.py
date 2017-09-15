from django.contrib import admin
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token
from api import views

user_list = views.ProfileViewSet.as_view({
    'get': 'list'
})

anon_list = views.AnonViewSet.as_view({
    'get': 'list'
})

user_detail = views.ProfileViewSet.as_view({
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

track_create = views.TrackViewSet.as_view({
    'post': 'create'
})

track_create_by_url = views.AddTrackByURLView.as_view()


urlpatterns = format_suffix_patterns([
    url(r'^o/token', obtain_jwt_token),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user-detail'),
    url(r'^oauth2/callback$', views.oauth2_callback, name='oauth2-callback'),
    url(r'^users/register$', views.RegisterUser.as_view(), name='user-register'),
    url(r'^anon/$', anon_list, name='anon-list'),
    url(r'^sessions/$', session_list, name='session-list'),
    url(r'^sessions/(?P<uuid>[0-9a-f-]+)/$', session_detail, name='session-detail'),
    url(r'^tracks/add/$', track_create, name='track-create'),
    url(r'^tracks/add_by_url/$', track_create_by_url, name='track-create-by-url'),
    url(r'^tracks/(?P<uuid>[0-9a-f-]+)/$', track_detail, name='track-detail'),
    url(r'^sms/$', views.sms),
    url(r'^$', views.api_root)

])



