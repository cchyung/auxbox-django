from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, detail_route
from api.serializers import *
from django.http import Http404, HttpResponse
from rest_framework import generics
from api.models import Session, Track
from django.contrib.auth.models import User
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


# Signup flow:
# 1. Front end gets authorization code from spotify
# 2. Front end hits callback endpoint which uses the auth. code to get access/refresh tokens
# 3. Logic to check if email has already been registered before
# 3.1 If not: create a user
# 4. Front end says "Great, we just need a little bit more information from you, asks for email and password"
# 6. Goes to sign up function, passes in email and password along with spotify tokens
#
# Note: Spotify access token is stored both locally and on the API, if the token is expired, the API will take care of
# updating with the refresh token and passing back the new spotify access token to the front end.
# Use: https://spotipy.readthedocs.io/en/latest/#module-spotipy.oauth2 see SpotifyOAuth Object for taking auth code

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


# Custom signup view
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




#
# class SessionList(generics.ListCreateAPIView):
# 	"""
# 	View to all the sessions in the database
# 	"""
#
# 	queryset = Session.objects.all()
# 	serializer_class = SessionSerializer
#
# class SessionDetail(APIView):
#
# 	queryset = Session.objects.all()
# 	serializer_class = SessionSerializer
# 	lookup_field = 'name'
#
#
# 	def get(self, request, name, format=None):
# 		"""
# 		Gets single session
# 		"""
# 		session = self.get_object(name)
# 		serializer = SessionSerializer(session)
# 		return Response(serializer.data)
#
# 	# Gets all sessions owned by user
#
# 	def get_queryset(self, username):
# 		"""
# 		Gets sessions specified by user
# 		"""
# 		user = self.kwargs('user')
# 		return Session.objects.filter(owner = User.objects.get(username=username))
#
# class SongList(generics.ListCreateAPIView):
# 	queryset = Song.objects.all()
# 	serializer_class = SongSerializer
