from rest_framework import serializers
from api.models import Track, Session
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='user-detail',
        # lookup_field='uuid'
    )

    sessions = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='session-detail',
        lookup_field='uuid'
    )

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'sessions')


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ('session', 'title', 'track_id')


class SessionSerializer(serializers.HyperlinkedModelSerializer):
    tracks = TrackSerializer(
        many=True,
        read_only=True,
    )

    url = serializers.HyperlinkedIdentityField(
        view_name='session-detail',
        lookup_field='uuid'
    )

    class Meta:
        model = Session
        fields = ('url', 'owner', 'name', 'tracks',)