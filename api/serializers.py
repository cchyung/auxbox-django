from rest_framework import serializers
from api.models import Track, Session
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    sessions = serializers.PrimaryKeyRelatedField(many=True, queryset=Session.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'sessions')


class SessionSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, queryset=Track.objects.all())
    owner = serializers.ReadOnlyField(source='owner.username')


    class Meta:
        model = Session
        fields = ('owner', 'name', 'slug', 'tracks',)
        read_only_fields = ('slug',)


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ('session', 'title', 'url')
