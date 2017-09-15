from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, detail_route
from api.serializers import *
from django.http import Http404, HttpResponse
from rest_framework import generics
from spotipy.oauth2 import SpotifyOAuth
from api.models import *
from rest_framework import permissions
from rest_framework.reverse import reverse
from django import db
import os
import services
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from twilio import twiml
from django_twilio.decorators import twilio_view
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime
import json
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import re
from services import parse_track_id


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


# class AnonView(generics.CreateAPIView):
#     queryset = Anon.objects.all()
#     serializer_class = AnonSerializer

#     def post(self, request, format=None):
#         serializer = AnonSerializer(data=request.data)
#         date_threshold = datetime.now() - timedelta(days = 30)
#         old = Anon.objects.filter(created_lt = date_threshold)
#         old.delete()
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Returns list of Annonymous users
class AnonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Anon.objects.all()
    serializer_class = AnonSerializer

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



#view for twilio sms testing
@twilio_view
def sms(request):
    """
    Keywords:

    'Join (4 letter key? or single word+numbers or something)' - Joins the session.  Allows the phone to makre requests to add songs.
    'Leave' (or join another session)' - Terminates the current connection to the session
    (User shares spotify share message) - Invalid when not in session, adds song to queue if in session.
    'Session' - Displays the current song queue in the session.  

    To-Do's
        Add "Session" functionality to display song queue, need oath with spotify to get the song names

    """
    r = MessagingResponse()
    text = request.POST.get('Body', '')
    number = request.POST.get('From', '')

    try:
        #Attempting to get anon user
        print "attempting to get anon user"
        qset = Anon.objects.filter(phone = number)      
        anon = next(iter(qset))
        serializer = AnonSerializer(anon)
        content = JSONRenderer().render(serializer.data)
        anon_content = json.loads(content)
        print anon_content["joined_session"] # Session of the current anon user
        #Anon Data
        curr_session = anon_content["joined_session"]
    except:
        #Anon Data
        curr_session = None

# -------------------------------------------------------------------------------

    # 'Join'
    if "join" in text.lower():
        session = text.lower().split()[-1]
        print session
        print "checking if session exists"
        if Session.objects.filter(name = session):
            print Session.objects.filter(name = session)
            msg = 'You just joined the session "%s"!  Text "Help me" for more actions, including how to add the song of your choice to this session! \n \n To leave this session, just text "leave".' % (session)
        else:
            msg = 'Sorry, I coudln\'t find a session with that name.'
            r.message(msg)
            return r

        create_dict = {'phone': number, 'added_date': datetime.today(), 'joined_session': session}
        try:
            #Deletes if number already exists in database linked with another session
            Anon.objects.filter(phone=number).delete()
            print 'Deleted an entry.'
        except:
            pass
        Anon.objects.create(**create_dict)
        r.message(msg)
        return r


# -------------------------------------------------------------------------------
    # (Shares a song from Spotify)
    # To-do's 
        # Add functionality to read back the actual song name to the user by requesting it from spotify
    if bool(re.search('(Here.s a song for you. .*\nhttps:\/\/open.spotify.com\/track\/.*|https:\/\/open.spotify.com\/track\/.*)', text)):
        if not curr_session:
            msg = 'It looks like you aren\'t part of a session yet! \n \n To join a session, simply message me \"join (session name)"! I\'ll look for this session, and add you to it.'
            r.message(msg)
            return r
        url = text.split()[-1]
        track = parse_track_id(url)
        print track
        msg = 'The song provided has been added to the session.  If you want to see the current song queue, just type "Session".'
        r.message(msg)
        return r


# -------------------------------------------------------------------------------
    #Help Commant
    if text.lower().split()[0] == "help" and text.lower().split()[1] == "me": 
        msg = 'To join a session, simply message me \"join (session name)"! I\'ll look for this session, and add you to it. \n The easiest way to add a song is to find your favorite song on the Spotify app and share it via text to me!  The text should look something like "Here\'s a song for you...." for me to understand it. \n\n To see the current session queue at any time, just text me "Sessions" and I\'ll show you the current queue! \n\n To Make your own session and to upvote and downvote songs, download the AuxBox app from the IOS App Store!'
        r.message(msg)
        return r

# -------------------------------------------------------------------------------
    #Leave 
    if text.lower().split()[-1] == 'leave':
        msg = 'You have been removed from the session "%s"' % (curr_session)
        try:
            #Pseudo for removing an anon user from the session, just deletes them from the database lol
            #This is totally fine though because it re-creates a database entry when number wants to join again
            Anon.objects.filter(phone=number).delete()
            print 'Deleted an entry.'
        except:
            pass

        r.message(msg)
        return r


# -------------------------------------------------------------------------------
    #Doesn't understand text
    else:
        r.message('I coudln\'t understand this request.  Text "Help me" for a list of available actions!')
        return r




#session = Session.objects.filter(name = anon_content["joined_session"])


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
>>>>>>> Sms
