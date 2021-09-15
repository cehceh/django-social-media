from rest_framework import viewsets
from rest_framework.response import Response
from media.models import *
from publish.models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponseNotFound
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required

# Create your views here.

class UsersViewSet(viewsets.ViewSet):
	def create(self, request):
		pass
	def list(self, request):
		serializer = UserSerializer(User.objects.all(), context = {'user': "Sb7", 'dumbb': "sb]", 'aaah': "asf,rlsa"}, many=True)
		return Response(serializer.data)

	def retrieve(self, request, pk):
		user = User.objects.get(pk=pk)
		serializer = UserSerializer(user, context = {'user': request.user, 'dumbb': "sb]", 'aaah': "asf,rlsa"})
		return Response(serializer.data)

class PostViewSet(viewsets.ModelViewSet):

	serializer_class = PostSerializer
	queryset = Post.objects.all()
	permission_classes = [IsAuthenticated]

	def create(self, request):
		serializer = PostSerializer(data=request.data)
		if serializer.is_valid():
			saved = serializer.save(author=request.user)
			return Response(PostSerializer(saved).data)
		return Response(serializer.errors)

	def list(self, request):
		posts = Post.objects.all()
		serializer = PostSerializer(posts, many=True)
		return Response(serializer.data)
	
	def retrieve(self, request, pk):
		post = Post.objects.get(pk=pk)
		serializer = PostSerializer(post)
		return Response(serializer.data)

	def delete(self, request, pk):
		post = Post.objects.get(pk=pk)
		post.delete()
 