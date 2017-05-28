from rest_framework import serializers
from api.models import Track, Session


class SessionSerializer(serializers.ModelSerializer):
	tracks = serializers.PrimaryKeyRelatedField(many=True, queryset=Track.objects.all())

	class Meta:
		model = Session
		fields = ('owner', 'name', 'tracks')


class TrackSerializer(serializers.ModelSerializer):

	class Meta:
		model = Track
		fields = ('session', 'title', 'url')
