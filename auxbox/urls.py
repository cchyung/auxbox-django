from django.contrib import admin
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
# from Auxy.views import UserList, SessionList, SessionDetail

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider'))
]
