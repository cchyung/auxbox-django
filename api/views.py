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
        'users': reverse('profile-list', request=request, format=format),
        'sessions': reverse('session-list', request=request, format=format)
    })


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


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


# Register user
@api_view(http_method_names=['POST'])
def register(request):
    # Get post data
    post_data = request.data

    # Validate presence of user data
    if all(member is not None for member in [
        post_data.get('username'),
        post_data.get('email'),
        post_data.get('password'),
        post_data.get('spotify_access_token'),
        post_data.get('spotify_refresh_token')
    ]):
        # Create user from data
        user = User(username=post_data['username'], email=post_data['email'], password=post_data['password'])
        try:
            user.save()
        except db.IntegrityError:
            return Response({"error": "This user already exists."})
        except db.Error:
            return Response({"error": "There was an error registering this user."})

        # Create profile from data
        profile = Profile(
            user=user,
            spotify_access_token=post_data['spotify_access_token'],
            spotify_refresh_token=post_data['spotify_refresh_token']
        )
        profile.save()

        return Response({
            "message": "Registration was a success!",
            "user": request.data})
    else:
        return Response({"error": "Information required to register is missing."})

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
        oauth_tool.refresh_access_token(token)
    else:
        return Response({"error": "Refresh token missing."})


class UserSignUp(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


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