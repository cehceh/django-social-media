from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .models import *
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
channel_layer = get_channel_layer()

@receiver(post_save, sender=Message)
def afterMessage(sender, instance, **kwargs):

	if not instance.sender in instance.receiver.chatted_with.all():
		instance.receiver.chatted_with.add(instance.sender)
		if not instance.receiver in instance.sender.chatted_with.all():
			instance.sender.chatted_with.add(instance.receiver)

	elif not instance.receiver in instance.sender.chatted_with.all():
		instance.sender.chatted_with.add(instance.receiver)
		if not instance.sender in instance.receiver.chatted_with.all():
			instance.receiver.chatted_with.add(instance.sender)

    

@receiver(post_delete, sender=Message)
def afterMessageDelete(sender, instance, **kwargs):
	message_group_name1 = 'chat_%d' % int(instance.receiver.pk + instance.sender.pk)
	message_group_name2 = 'chat_%d' % int(instance.receiver.pk + instance.sender.pk)

	async_to_sync(channel_layer.group_send)(
        message_group_name1,
        {'type': 'chat_message', 'delete': instance.pk})
	
	async_to_sync(channel_layer.group_send)(
        message_group_name2,
        {'type': 'chat_message', 'delete': instance.pk})