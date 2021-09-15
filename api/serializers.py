from rest_framework import serializers
from media.models import User
from publish.models import *
class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		exclude = ('password',)

class PostSerializer(serializers.ModelSerializer):
	author = serializers.SerializerMethodField(method_name="author_serializer")

	def author_serializer(self, post):
		return UserSerializer(post.author, read_only=True).data

	class Meta:
		model = Post
		fields = '__all__'