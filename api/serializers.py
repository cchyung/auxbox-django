from rest_framework import serializers
from api.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')

    def create(self, validated_data):
        user = User.objects.create(email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user

class AnonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anon
        fields = '__all__'


class UserDetailSerializer(serializers.ModelSerializer):
    sessions = serializers.HyperlinkedRelatedField(
        view_name='session-detail',
        lookup_field='uuid',
        many=True,
        read_only=True
    )

    class Meta:
        model = User
        fields = ('email', 'sessions')


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