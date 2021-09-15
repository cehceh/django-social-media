from rest_framework import routers
from .views import *
from django.urls import path
router = routers.DefaultRouter()

router.register('Users', UsersViewSet, 'getUser')
router.register('posts', PostViewSet, 'getUser')
#router.register('post/likes/', LikeButton, 'postLike')

funs = [
]