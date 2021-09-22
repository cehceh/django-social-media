from django.db import models
from django.conf import settings
from datetime import datetime

# Create your models here.
def MessageMediaStorage(instance, filename):
	return 'messages/room-{0}/{1}'.format(str(int(instance.message.sender.id) + int(instance.message.receiver.id)), filename)

def MessageRecordStorage(instance, filename):
	return 'messages/room-{0}/{1}'.format(str(int(instance.sender.id) + int(instance.receiver.id)), filename)

def AnonymousMessageMediaStorage(instance, filename):
	return 'anonymous_messages/{0} to {1}/{2}'.format(instance.message.sender, instance.message.receiver, filename)


class Message(models.Model):

	sender 		= models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name='message_sender')

	receiver 	= models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name='message_receiver')

	content = models.CharField(null=True, blank=True, max_length=255)
	record		= models.FileField(null=True, blank=True, upload_to = MessageRecordStorage,)
	
	date 		= models.DateTimeField(auto_now_add=True)
	reply 		= models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='m_replies')
	room 		= models.ForeignKey('AnonymousRoom', null=True, blank=True, on_delete=models.CASCADE, related_name='anonymous_messages')
	is_seen		= models.BooleanField(default=False)

	def __str__(self):
		return str(self.id)

	def sent(self):
		time = datetime.now()
		if self.date.day == time.day:
			return str(time.hour - self.date.hour) + " hours ago"
		else:
			if self.date.month == time.month:
				return str(time.day - self.date.day) + " days ago"
			else:
				if self.date.year == time.year:
					return str(time.month - self.date.month) + " months ago"
		return self.date


class MessageMedia(models.Model):
	message 	= models.ForeignKey(Message, null=True, blank=True, on_delete=models.CASCADE, related_name='messageMedia')
	media 		= models.FileField(upload_to  = MessageMediaStorage, null=True)
	


class AnonymousRoom(models.Model):
	creator 	= models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name='anonymous_room_creator')

	partner 	= models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name='not_anonymous_room_partner')

	def delete(self):
		self.delete()




