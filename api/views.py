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


class AnonView(generics.CreateAPIView):
    queryset = Anon.objects.all()
    serializer_class = AnonSerializer

    def post(self, request, format=None):
        serializer = AnonSerializer(data=request.data)
        date_threshold = datetime.now() - timedelta(days = 30)
        old = Anon.objects.filter(created_lt = date_threshold)
        old.delete()
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
@csrf_exempt
def sms(request):
    twiml = '<Response><Message>Hello from your Django app!</Message></Response>'
    return HttpResponse(twiml, content_type='text/xml')




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
