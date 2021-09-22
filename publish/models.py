from django.db import models
from django.conf import settings
import media.models as media
from datetime import datetime
import re


def get_post_upload_path(instance, filename):
	return 'posts/{0}/{1}/{2}'.format(instance.post.author.email, instance.post.id ,filename)

def get_comment_file_path(instance, filename):
	return 'comments/{0}/{1}'.format(instance.post.author.email, instance.post.id ,filename)

def get_reply_file_path(instance, filename):
	return 'replies/{0}/{1}'.format(instance.post.author.email, instance.post.id ,filename)
# Create your models here.

class CustomFK(models.ForeignKey):
	def contribute_to_class(self, cls, name, private_only=False, **kwargs):
		super().contribute_to_class(cls, name, private_only=False, **kwargs)
		self.remote_field.related_name = "_".join(re.findall('[A-Z][^A-Z]*', cls.__name__))

class Snippet(models.Model):
	content = models.TextField()
	author 			= CustomFK(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name='%(class)s')
	post 			= CustomFK('Post', null=True, blank=True, on_delete=models.CASCADE, related_name='%(class)s')
	likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='%(app_label)s_likes_%(class)s', related_query_name='%(app_label)s_likes_%(class)s')
	love = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='%(app_label)s_love_%(class)s', related_query_name='%(app_label)s_love_%(class)s')
	sad = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='%(app_label)s_sad_%(class)s', related_query_name='%(app_label)s_sad_%(class)s')
	wow = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_query_name='%(app_label)s_wow_%(class)s', related_name='%(app_label)s_wow_%(class)s')
	haha = models.ManyToManyField(settings.AUTH_USER_MODEL,  blank=True, related_name='%(app_label)s_haha_%(class)s', related_query_name='%(app_label)s_haha_%(class)s')
	angry = models.ManyToManyField(settings.AUTH_USER_MODEL,  blank=True,related_query_name='%(app_label)s_angry_%(class)s', related_name='%(app_label)s_angry_%(class)s')
	shared = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='%(app_label)s_shared_%(class)s', related_query_name='%(app_label)s_shared_%(class)s')
	DatePublished = models.DateTimeField(auto_now_add=True)

	def date(self):
		time = datetime.now()
		if self.DatePublished.day == time.day:
			return str(time.hour - self.DatePublished.hour) + " hours ago"
		else:
			if self.DatePublished.month == time.month:
				return str(time.day - self.DatePublished.day) + " days ago"
			else:
				if self.DatePublished.year == time.year:
					return str(time.month - self.DatePublished.month) + " months ago"
		return self.DatePublished  

	def reacts_count(self):
		reacts = int(self.likes.count()) + int(self.love.count())+ int(self.sad.count())+ int(self.wow.count())+ int(self.haha.count())+ int(self.angry.count())

		if reacts == 1:
			return str("1 React")

		else:
			return str(reacts) + " Reacts" 

	class Meta:
		abstract = True
		ordering = ['-DatePublished']		

	def __str__(self):
		return self.content

class Post(Snippet):
	group 			= models.ForeignKey('media.Group', null=True, blank=True, on_delete=models.CASCADE , related_name='post_group')
	accepted		= models.BooleanField(default=True)

	page 			= models.ForeignKey('media.Page', null=True, blank=True, on_delete=models.CASCADE , related_name='post_page')
	fixed = models.BooleanField(default=False)
	post_notify_people = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='post_notified_users')


class PostFiles(Snippet):
	media = models.FileField(upload_to=get_post_upload_path, blank=True, null=True)


class Comment(Snippet):
	reply = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='replies')
	repo = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='snippets')
	media = models.FileField(upload_to=get_post_upload_path, blank=True, null=True)


	 
	 

