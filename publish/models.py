from django.db import models
from django.conf import settings
import media.models as media
from datetime import datetime



def get_post_upload_path(instance, filename):
	return 'posts/{0}/{1}/{2}'.format(instance.post.author.email, instance.post.id ,filename)

def get_comment_file_path(instance, filename):
	return 'comments/{0}/{1}'.format(instance.post.author.email, instance.post.id ,filename)

def get_reply_file_path(instance, filename):
	return 'replies/{0}/{1}'.format(instance.post.author.email, instance.post.id ,filename)
# Create your models here.

class Post(models.Model):
	
	author 			= models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name='post_author')
	
	group 			= models.ForeignKey('media.Group', null=True, blank=True, on_delete=models.CASCADE , related_name='post_group')
	accepted		= models.BooleanField(default=True)

	page 			= models.ForeignKey('media.Page', null=True, blank=True, on_delete=models.CASCADE , related_name='post_page')

	content		 	= models.CharField(max_length=500)

	DatePublished 	= models.DateTimeField(auto_now_add=True)

	fixed = models.BooleanField(default=False)

	share = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='shared_post')

	post_notify_people = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='post_notified_users')

	likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='blogpost_like', blank=True)
	love = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='blogpost_love',  blank=True)
	sad = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='blogpost_sad',  blank=True)
	wow = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='blogpost_wow', blank=True)
	haha = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='blogpost_haha',  blank=True)
	angry = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='blogpost_angry',  blank=True)
	shared = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='post_share_users', blank=True)
	class Meta:
		ordering = ['-DatePublished']


	def reacts_count(self):
		reacts = int(self.likes.count()) + int(self.love.count())+ int(self.sad.count())+ int(self.wow.count())+ int(self.haha.count())+ int(self.angry.count())

		if reacts == 1:
			return str("1 React")

		else:
			return str(reacts) + " Reacts" 

		

	def __str__(self):
		return self.content


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




class PostFiles(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_file')
	caption = models.CharField(max_length=300 , null=True, blank=True)
	media = models.FileField(upload_to=get_post_upload_path, blank=True, null=True)







class Comment(models.Model):
	
	post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE, blank=True, null=True)
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	content = models.TextField()
	DatePublished = models.DateTimeField(auto_now_add=True)
	
	reply = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='replies')
	snippet = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='snippets')

	media = models.FileField(upload_to=get_post_upload_path, blank=True, null=True)
	record = models.FileField(upload_to=get_post_upload_path, blank=True, null=True)


	likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='comment_like', blank=True)
	love = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='comment_love',  blank=True)
	sad = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='comment_sad',  blank=True)
	wow = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='comment_wow', blank=True)
	haha = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='comment_haha',  blank=True)
	angry = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='comment_angry',  blank=True)
	

	def __str__(self):
		return self.content
	 
	def reacts_count(self):
		reacts = int(self.likes.count()) + int(self.love.count())+ int(self.sad.count())+ int(self.wow.count())+ int(self.haha.count())+ int(self.angry.count())
		if reacts == 0:
			return str("")

		elif reacts == 1:
			return str("1 React")

		else:
			return (str(reacts), " Reacts" )

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

