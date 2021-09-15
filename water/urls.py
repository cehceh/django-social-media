"""water URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from media import views as media_views
from chat import views as chat_views
from publish import views as publish_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import static
from django.contrib.auth import views as auth
from django.views.generic import *
from api.routes import router, funs

urlpatterns = [

	path('apkmjpaqojkqp[akrf[eqakr[qek,rtqe', media_views.Blocked, name='blocked'),

	path('admin/', admin.site.urls),
	path('streaming/', chat_views.Streaming),
	path('accounts/login/', media_views.loginView, name="auth"),
	path('accounts/signup/', media_views.SignUp, name="signup"),
	path('accounts/', include('django.contrib.auth.urls')),
	path('allauth/', include('allauth.urls')),

	path('chaining/', include('smart_selects.urls')),

	##Basic Media
	path('', media_views.HomeView, name="home"),
	path('post/<int:pk>', publish_views.PostDetail, name='post'),
	path('profile/<int:pk>', media_views.ProfileView, name="profile"),
	path('page/<int:pk>', media_views.PageView, name="page"),
	path('notify/<int:pk>/href', media_views.NotifyHref, name="notify-href"),
	path('friends', media_views.UserFriendsPage, name='friends'),
	path('group/<int:pk>', media_views.GroupView, name="group"),
	path('group/<int:pk>/rules', media_views.GroupRulesView, name="group-rules"),
	path('group/<int:pk>/join-or-cancel/request', media_views.GroupRequestsView, name="group-request"),
	path('leave/group/<int:pk>', media_views.LeaveGroupView, name="leave-group"),
	path('see/group/<int:pk>/fixed-posts', media_views.GroupFixedPosts, name='group-fixed-posts'),
	path('group-<int:pk>/members', media_views.GroupMembersView, name='group-members'),
	path('group/<int:pk>/posts-permission', media_views.GroupPostsPerm, name='group-posts-permissions'),
	path('group/<int:group_id>/member/<int:user_id>/group-profile', media_views.GroupMemberProfile, name='GroupMemberProfile'),
	path('get/group/number/<int:pk>/members/', media_views.GetGroupMembers, name='get-members'),
	path('search', media_views.SearchView, name='search'),
	path("modify-search/<int:pk>/type-<int:_type>/searched-<int:searchedPK>", media_views.ModifySearch, name='modify-search'),
	path('user-groups', media_views.UserGroups, name='user-groups'),
	path('create-group', media_views.CreateGroup, name='create-group'),
	path('accept/user/group/join/request/', media_views.AcceptGroupJoinReq, name='accept-group-request'),
	path('deny/user/group/join/request/', media_views.DenyGroupJoinReq, name='deny-group-request'),
	##FriendShip
	path('add-user/number-<int:pk>', media_views.AddFriendView, name="add-friend"),
	path('remove-user/number-<int:pk>', media_views.RemoveFriendView, name="remove-friend"),
	path('block-user/number-<int:pk>', media_views.BlockUser, name="block-user"),
	path('follow-user/<int:pk>', media_views.FollowUser, name="follow-user"),


	##Friend Request Actions
	path('accept/friend-request/number-<int:pk>', media_views.AcceptFriend, name="accept-friend-request"),
	path('deny/friend-request/number-<int:pk>', media_views.DenyFriend, name="deny-friend-request"),
	path('cancel/friend-request/number-<int:pk>', media_views.CancelRequest, name="cancel-friend-request"),


	path('crush-on-user/number-<int:pk>', media_views.CrushOnUser, name="crush"),

	##publish
	
	#Posting
	path('post', publish_views.CreatePost, name='post'),
	path('comment/<int:pk>', publish_views.CreateComment, name='comment'),
	path('share/post/<int:pk>', publish_views.SharingPost, name='share-post'),

	#getting stuff
	path('get/10-comments/on/post-number/<int:pk>/<int:counts>', publish_views.GetPostComment, name='get-comments'),
	path('get/10-posts/<int:counts>', publish_views.GetPosts, name='get-posts'),


	path('save/post/', publish_views.SavePost, name='save-post'),
	path('activate/post/<int:pk>/notifies', publish_views.ActivatePostNotify, name='open-post-notifies'),


	##Reacting
	path('remove-react/on/post-number/<int:pk>', publish_views.RemovePostReact, name='remove-post-react'),

	path('like/post-number/<int:pk>', publish_views.LikePost, name='like-post'),
	path('love/post-number/<int:pk>', publish_views.LovePost, name='love-post'),
	path('haha/post-number/<int:pk>', publish_views.SmilePost, name='haha-post'),
	path('sad/post-number/<int:pk>', publish_views.SadPost, name='sad-post'),
	path('angry/post-number/<int:pk>', publish_views.AngryPost, name='angry-post'),
	path('wow/post-number/<int:pk>', publish_views.WowPost, name='wow-post'),
	


	#modefying
	path('delete/post/number-<int:pk>', publish_views.DeletePost, name='delete-post'),
	path('update/post/number-<int:pk>', publish_views.UpdatePost, name='update-post'),

	##Chat
	#normal
	path('chat/<int:partner_id>', chat_views.MessageView, name="messages"),
	path('chat/send-messages/', chat_views.SendMessageView, name="send-message"),
	path('delete/message/', chat_views.DeleteMessage, name="delete-message"),
	#anonymous
	path('AnonymousChat/<int:pk>', chat_views.AnonymousChatView, name="AnonymousChat"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + router.urls + funs
