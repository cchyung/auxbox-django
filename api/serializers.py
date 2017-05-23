from rest_framework import serializers
# from api.models import Song, Session, User


# class UserSerializer(serializers.ModelSerializer):
# 	sessions = serializers.PrimaryKeyRelatedField(many=True, queryset=Session.objects.all(), required=False)
#
# 	class Meta:
# 		model = User
# 		fields = ('username', 'serial', 'sessions')
#
# class SessionSerializer(serializers.ModelSerializer):
# 	songs = serializers.PrimaryKeyRelatedField(many=True, queryset=Song.objects.all(), required=False)
#
# 	class Meta:
# 		model = Session
# 		fields = ('name', 'owner', 'songs')
#
#
# class SongSerializer(serializers.ModelSerializer):
#
# 	class Meta:
# 		model = Song
# 		fields = ('title', 'artist', 'cur_session', 'like', 'id')
