from django.contrib import admin
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = format_suffix_patterns([
	url(r'^user/', views.UserList.as_view()),
	url(r'^sessions/', views.SessionList.as_view()),
	url(r'^/', views.SessionDetail.as_view()),
	url(r'^songs/', views.SongList.as_view()),

])