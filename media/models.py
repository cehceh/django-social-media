from django.db.models import *
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from .manager import UserManager
from django.urls import reverse
from smart_selects.db_fields import ChainedForeignKey

# Create your models here.



def get_profile_cover_path(instance, filename):
	return 'profiles/{0}/cover/{1}'.format(instance.email, filename)

def get_profile_pic_path(instance, filename):
	return 'profiles/{0}/pic/{1}'.format(instance.email, filename)

def get_page_img_path(instance, filename):
	return 'images/{0}/{1}'.format(instance.page_name, filename)

def get_group_img_path(instance, filename):
	return 'groups/{0}/{1}'.format(instance.group_name, filename)

class Country(Model):
	name = CharField(max_length=100)

	def __str__(self):
		return self.name

class Government(Model):
	name = CharField(max_length=100)
	country = ForeignKey(Country, null=True, blank=True, on_delete=CASCADE, related_name='countryGoverns')

	def __str__(self):
		return "{0} of {1}".format(self.name, self.country.name)

class User(AbstractBaseUser, PermissionsMixin):
	gender_type = ((1, 'Male'), (2, 'Female'))
	#country = ForeignKey(Country, null=True, blank=True, on_delete=CASCADE, related_name='countryUsers')
	#city = ChainedForeignKey(
	#	Government,
	#	chained_field="country",
	#	chained_model_field="country",
	#	show_all=False,
	#	auto_choose=True,
	#	sort=True, null=True)
	email = EmailField(('email address'), unique=True, null=True, blank=False)
	name = CharField(('name'), max_length=25, blank=True, null=True)
	date_joined = DateTimeField(('date joined'), auto_now_add = True, blank=True, null=True)
	is_active = BooleanField(('active'), default=True)
	is_online = BooleanField(('online'), default=True)
	BirthDate = DateTimeField(auto_now_add=False, blank=True, null=True)
	gender = IntegerField(choices=gender_type, null=True)
	bio 	= CharField(max_length=100, blank=True, null=True)
	avatar 	= ImageField(upload_to = get_profile_pic_path, null = True, blank = True,)
	cover_pic 	= ImageField(upload_to = get_profile_cover_path, null = True, blank = True,)
	following = ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='user_following')
	followers = ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='user_followers')
	friends = ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='user_friends')
	blocked = ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='user_blocked')
	waiting = ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='user_waiting')
	waiting_for = ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='user_waiting_for')
	validated = BooleanField(default=False)
	saved_posts = ManyToManyField('publish.Post', blank=True , related_name='user_saved_posts')
	groups = ManyToManyField('Group', blank=True, related_name='users_groups')
	pages = ManyToManyField('Page', blank=True, related_name='users_pages')
	allow_anonymous = BooleanField(default=True)
	crush	= ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='user_crush')
	is_superuser = BooleanField(('superuser'), default=False)
	is_admin = BooleanField(('admin'), default=False)
	is_staff = BooleanField(('staff'), default=False)
	chatted_with = ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELD = []

	def pic(self):
		if not self.avatar:
			return '/images/profiles/profile.jpg'
		return self.avatar

	def cover(self):
		if not self.cover_pic:
			return '/images/profiles/cover.jpg'
		return self.cover_pic

	def full_name(self):

		return self.name
	def first_name(self):
		return self.name.split()[0]

	def __str__(self):
		if not self.name:
			self.name = self.email.split('@')[0]
		return str(self.id) + ": " + self.full_name()

class Group(Model):
	group_admin = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name='group_author', null=True, blank=True)
	group_sub_admin = ManyToManyField(settings.AUTH_USER_MODEL, related_name='group_sub_author', blank=True)
	group_cover_photo = ImageField(upload_to=get_group_img_path, null=True, blank=True)
	group_name  = TextField()
	group_members = ManyToManyField(settings.AUTH_USER_MODEL, related_name='group_members', blank=True)
	group_members_waiting = ManyToManyField(settings.AUTH_USER_MODEL, related_name='group_waiting_members', blank=True)
	invite_group_members = ManyToManyField(settings.AUTH_USER_MODEL, related_name='invited_group_members', blank=True)
	group_members_blocked = ManyToManyField(settings.AUTH_USER_MODEL, related_name='group_blocked_members', blank=True)

	def get_absolute_url(self):
		return "/group/%i" % self.id

	def __str__(self):
		return self.group_name
 

class Page(Model):
	page_admin = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name='page_author', null=True, blank=True)
	page_sub_admin = ManyToManyField(settings.AUTH_USER_MODEL, related_name='page_sub_author', blank=True)
	page_photo = ImageField(upload_to=get_page_img_path, null=True, blank=True)
	page_cover_photo = ImageField(upload_to=get_page_img_path, null=True, blank=True)
	page_name  = TextField()
	page_bio   = TextField(null=True, blank=True)
	page_likes = ManyToManyField(settings.AUTH_USER_MODEL, related_name='page_like', blank=True)
	page_blocked_members = ManyToManyField(settings.AUTH_USER_MODEL, related_name='page_blocked_members', blank=True)
	validated = BooleanField(default=False)

	def get_absolute_url(self):
		return "/page/%i" % self.id

	def __str__(self):
		return self.page_name



class UserCrushs(Model):
	user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name="crusher", blank=True, null=True )

	crush = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name="crushed", blank=True, null=True )


class Notifications(Model):

	NOTIFICATION_TYPES = ((1, 'Likes'), (2, 'Love'), (3, 'Haha'), (4, 'Sad'), (5, 'Wow'), (6, 'Angry'), (7, 'Comment'), (8, 'Reply'), (9, 'Share'), (10, 'follow'), (11, 'crush'), (12, 'invite'))

	NOTIFICATION_OBJECT = ((1, 'Post'), (2, 'Comment'), (3, 'Reply'), (4, 'Page'), (5, 'Group'))
   
	post = ForeignKey('publish.Post', on_delete=CASCADE, related_name="notif_post", blank=True, null=True )
	sender = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name="notif_post_from_user",  blank=True, null=True )
	receiver = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name="notif_post_to_user",  blank=True, null=True )
	notifications_type = IntegerField(choices=NOTIFICATION_TYPES, null=True)
	notifications_obj = IntegerField(choices=NOTIFICATION_OBJECT, null=True)
	text_preview = CharField(max_length=90, blank=True)
	is_seen = BooleanField(default=False)
	react = BooleanField(default=False)
	comments = ForeignKey('publish.Comment', on_delete=CASCADE, blank=True, null=True, related_name='notify_comment')
	is_comment = BooleanField(default=False)
	is_reply = BooleanField(default=False)
	when = DateTimeField(auto_now_add=True)
	group 			= ForeignKey(Group, null=True, blank=True, on_delete=CASCADE , related_name='notify_group')
	page 			= ForeignKey(Page, null=True, blank=True, on_delete=CASCADE , related_name='notify_page')

	class Meta:
		ordering = ['-when']


class Search(Model):
	SearchObject = ((1, 'Post'), (2, 'Page'), (3, 'User'), (4, 'Group'))

	object_type 	= IntegerField(null=True, choices=SearchObject)
	searcher = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, blank=True, null=True, related_name='searcher')
	searched = CharField(max_length=100)
	user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, blank=True, null=True, related_name='searched_user')
	page = ForeignKey(Page, null=True, blank=True, on_delete=CASCADE, related_name='searched_page')
	group = ForeignKey(Group, null=True, blank=True, on_delete=CASCADE, related_name='searched_group')
	date 	 = DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.searcher.full_name() + " searched for " + self.searched + " on " + str(self.date)