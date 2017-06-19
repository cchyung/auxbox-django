from rest_framework import serializers
from api.models import Track, Session
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    sessions = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='session-detail',
        lookup_field='uuid'
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'sessions')


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ('session', 'title', 'url')


class SessionSerializer(serializers.HyperlinkedModelSerializer):
    tracks = TrackSerializer(
        many=True,
        read_only=True,
    )

    session_url = serializers.HyperlinkedIdentityField(
        view_name='session-detail',
        lookup_field='uuid'
    )

    class Meta:
        model = Session
        fields = ('session_url', 'owner', 'name', 'tracks',)
