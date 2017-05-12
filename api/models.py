from __future__ import unicode_literals
from django.db import models
import uuid


class User(models.Model):
	# Each user has username, pulled from Spotify IOS SDK (Spotify Username (facebook?))
	username = models.CharField(max_length=30, primary_key=True) #Name of user 
	serial = models.UUIDField(default=uuid.uuid4, editable=False) #unique ID

	def __str__(self):
		return str(self.username)

class Session(models.Model):
	name = models.CharField(max_length=50)
	owner = models.ForeignKey('api.User', help_text='Linked User', default=None) #Users can have multiple Sessions


	def __str__(self):
		return str(self.name)

		#Things to think about: 
		#	Will sessions be deleted after a single use, or
		#	can one keep a session (and therefore the songs in the session)
		#	for later use?



class Song(models.Model):
	#Pulls from IOS Spotify SDK and fills Song title, Artist, Album, and unique id for reference 
	# Also fills Current session, Likes/dislikes as a number
	title = models.CharField(max_length=50)
	artist = models.CharField(max_length=50)
	cur_session = models.ForeignKey('api.Session', help_text='Session', default=None)#Connects songs related session when created
	like = models.IntegerField()#starts at 0, +num for upvotes and -num for downvotes, used to sort session tracks
	id = models .CharField(primary_key=True, max_length=40) #Spotify track id form SDK used to play song

	def __str__(self):
		return str(self.title)
