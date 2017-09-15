from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, detail_route
from api.serializers import *
from django.http import Http404, HttpResponse
from rest_framework import generics
from api.models import Session, Track, User
from spotipy.oauth2 import SpotifyOAuth
from rest_framework import permissions
from rest_framework.reverse import reverse
from django import db
import os
import services

# Root view for API
# Returns url to users and sessions
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'message': 'Welcome to the AuxBox API!',
        'sessions': reverse('session-list', request=request, format=format)
    })

# OAuth Callback
@api_view(http_method_names=['GET'])
def oauth2_callback(request):
    # Get auth code or error
    authorization_code = request.GET.get('code')
    error = request.GET.get('error')

    if (authorization_code):  # Success!
        # Get access/refresh token with authorization code
        oauth_tool = SpotifyOAuth(
            os.environ['SPOTIFY_CLIENT_ID'],
            os.environ['SPOTIFY_SECRET_KEY'],
            # reverse('api:oauth2-callback')
            'http://localhost:8000/api/oauth2/callback' # TODO update this to handle reverse
        )

        access_info = oauth_tool.get_access_token(authorization_code)
        return Response(access_info)

    else:  # Failure (User denied authorization request or other error)
        return Response({
            "error": error,
            "message": "Error with authentication"
        })


@api_view(http_method_names=['GET'])
def refresh_token(request):
    # Get post data
    post_data = request.data
    if post_data.get('spotify_refresh_token') is not None:
        oauth_tool = SpotifyOAuth(
            os.environ['SPOTIFY_CLIENT_ID'],
            os.environ['SPOTIFY_SECRET_KEY'],
            # reverse('api:oauth2-callback')
            'http://localhost:8000/api/oauth2/callback'
        )

        token = post_data.get('spotify_refresh_token')
        data = oauth_tool.refresh_access_token(token)
        # update user's data
    else:
        return Response({"error": "Refresh token missing."})


class RegisterUser(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


# Returns list of sessions
class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    lookup_field = 'uuid'


# Returns list of sessions
class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    lookup_field = 'uuid'


class AddTrackByURLView(generics.CreateAPIView):
    serializer_class = TrackSerializer

    def perform_create(self, serializer):
        serializer.save(track_id=services.parse_track_id(self.request.data.get('url')))