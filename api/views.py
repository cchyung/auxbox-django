from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, detail_route
from api.serializers import *
from django.http import Http404, HttpResponse
from rest_framework import generics
from api.models import Session, Track, Anon
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.reverse import reverse
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
        'users': reverse('profile-list', request=request, format=format),
        'sessions': reverse('session-list', request=request, format=format)
    })


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class UserSignUp(generics.CreateAPIView):
    serializer_class = UserSerializer


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
    'STOP (or join another session)' - Terminates the current connection to the session
    (User shares spotify share message) - Invalid when not in session, adds song to queue if in session.
    'Session' - Displays the current songs in the session.  

    """
    r = MessagingResponse()
    text = request.POST.get('Body', '')
    number = request.POST.get('From', '')


    #Attempting to get anon user
    print "attempting to get anon user"
    qset = Anon.objects.filter(phone = number)      
    anon = next(iter(qset))
    serializer = AnonSerializer(anon)
    content = JSONRenderer().render(serializer.data)
    anon_content = json.loads(content)
    print anon_content["joined_session"] # Session of the current anon user


    # 'Join'
    if "join" in text.lower():
        session = text.lower().split()[-1]
        print session
        print "checking if session exists"
        if Session.objects.filter(name = session):
            print Session.objects.filter(name = session)
            msg = 'You just joined the session "%s"!  Text "Help me" for more actions, including how to add the song of your choice to this session!' % (session)
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

    # (Shares a song from Spotify)
    if bool(re.search('(Here.s a song for you. .*\nhttps:\/\/open.spotify.com\/track\/.*|https:\/\/open.spotify.com\/track\/.*)', text)):

        msg = 'The song provided has been added to the session.  If you want to see the current song queue, just type "Session".'
        r.message(msg)
        return r


    if 'help me' in text.lower():
        msg = 'To join a session, simply message me \"join (session name)"! I\'ll look for this session, and add you to it. \n The easiest way to add a song is to find your favorite song on the Spotify app and share it via text to me!  The text should look something like "Here\'s a song for you...." for me to understand it.  \n To see the current session queue at any time, just text me "Sessions" and I\'ll show you the current queue!'
        r.message(msg)
        return r


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
