from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.auth.models import User
from .models import *
from media.models import Notifications

@receiver(post_save, sender=Comment)
def afterComment(sender, instance, created, **kwargs):
	if not instance.author == instance.post.author:
		post = instance.post
		if post.comments.count() == 1:
			for receiver in post.post_notify_people.all():
				text_preview = "{0} commented on your post {1}".format(instance.author.full_name(), post.content)
				Notifications.objects.create(sender=instance.author, text_preview=text_preview, receiver=receiver, notifications_type=7, notifications_obj=2, post=post, comments=instance)
		else:
			for receiver in post.post_notify_people.all():
				text_preview = "{0} and {1} others commented on your post {2}".format(instance.author.full_name(), post.comments.count() , post.content)
				Notifications.objects.create(sender=instance.author, text_preview=text_preview, receiver=receiver, notifications_type=7, notifications_obj=2, post=post, comments=instance)
@receiver(post_save, sender=Post)
def afterPost(sender, instance, **kwargs):
	instance.post_notify_people.add(instance.author)