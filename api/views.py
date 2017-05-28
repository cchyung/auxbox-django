from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from api.serializers import SessionSerializer, TrackSerializer
from django.http import Http404, HttpResponse
from rest_framework import generics
from api.models import Session, Track
from django.contrib.auth.models import User
from rest_framework import permissions


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'response': 'Hello World!'
    })

class SessionList(generics.ListAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer



# class UserList(generics.ListCreateAPIView):
#
# 	queryset = User.objects.all()
# 	serializer_class = UserSerializer
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
