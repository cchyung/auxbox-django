from rest_framework import serializers
from api.models import Track, Session, Profile
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name','username', 'email')

    def create(self, validated_data):
        # Create profile with new user
        user = User(**validated_data)
        profile = Profile(user=self.instance)
        profile.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='profile-detail',
        # lookup_field='uuid'
    )

    sessions = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='session-detail',
        lookup_field='uuid'
    )

    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ('url', 'user', 'sessions', 'spotify_access_token', 'spotify_refresh_token')


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ('session', 'track_id')


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