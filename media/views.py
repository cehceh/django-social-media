from django.shortcuts import render, get_object_or_404
from .models import *
from .forms import * 
from publish.forms import *
from publish.models import *
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django import template
from django.template import *
from django.db.models import Q
from channels.layers import get_channel_layer
from collections import Counter
from .forms import SignUpForm
import itertools
from asgiref.sync import async_to_sync
from django.template.loader import render_to_string

channel_layer = get_channel_layer()

@login_required
def UserGroups(request):
	return render(request, 'unique/groups.html')

@login_required
def CreateGroup(request):
	form = GroupForm(request.POST or None, request.FILES or None)
	if request.method == 'POST':
		if form.is_valid():
			form = form.save(commit=False)
			form.group_admin = request.user
			form.save()
			return HttpResponseRedirect((reverse('group', args=[str(form.pk),])))
		else:
			return render(request, 'forms/group.html', {'form': form})
	else:
		return render(request, 'forms/group.html', {'form': form})

def AddUserToCookies(request, _id,  url):
	if request.is_ajax():
		response = JsonResponse({'done':True})
	else:
		response = HttpResponseRedirect((reverse(url)))

	cookies = request.COOKIES.get('users' or None)
	
	email = _id

	if cookies:
		if not str(email) in str(cookies):
			cookies += str(" %s"% email)
			response.set_cookie('users', cookies, max_age = 6048000)
	else:
		cookies = str(" %s"% email)
		response.set_cookie('users', cookies, max_age = 6048000)
	return response

def loginView(request):
	if not request.user.is_authenticated:
		loginForm = AuthenticationForm(data = request.POST or None)
		signup = SignUpForm()
		users = []
		usersC = request.COOKIES.get('users' or None)
		if usersC:
			for user in usersC.split():
				users.append(User.objects.get(id=user))
		if not request.method == 'POST':
			return render(request, 'registration/login.html', {'login': loginForm, 'signup': signup, 'users': users})
		else:
			if loginForm.is_valid():
				user = authenticate(request, email=request.POST['username'], password=request.POST['password'])
				login(request, user)
				return AddUserToCookies(request, user.id, 'home')
			else:
				print("not valid")
				if request.is_ajax():
					return JsonResponse({'failure': True})
				return render(request, 'registration/login.html', {'login': loginForm, 'signup': signup, 'users': users})
	else:
		return HttpResponseRedirect((reverse('home')))


def SignUp(request):
	form = SignUpForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			user = form.save()
			user = authenticate(request, email=form.cleaned_data['email'], password=form.cleaned_data['password1'])
			login(request, user)
			return AddUserToCookies(request, user.id, 'home')
		else:
			loginForm = AuthenticationForm()
			users = []
			usersC = request.COOKIES.get('users' or None)
			if usersC:
				for user in usersC.split():
					users.append(User.objects.get(id=user))
			return render(request, 'registration/login.html', {'login': loginForm, 'signup': form, 'users': users})
	else:
		return HttpResponseRedirect((reverse('auth')))


@login_required
def NotifyHref(request, pk):
	notify = get_object_or_404(Notifications, pk=pk)
	if notify.page:
		return HttpResponseRedirect((reverse('page', args=[str(notify.page.pk)])))
	elif notify.group:
		return HttpResponseRedirect((reverse('group', args=[str(notify.group.pk)])))
	elif notify.post:
		return HttpResponseRedirect((reverse('post', args=[str(notify.post.pk)])))
	else:
		return HttpResponseRedirect((reverse('profile', args=[str(notify.sender.pk)])))

@login_required
def HomeView(request):
	counter = request.GET.get("counter" or None)
	posts = Post.objects.filter((Q(author = request.user) | Q(author__in = request.user.friends.all()) | Q(author__in = request.user.following.all()) | Q(group__in = request.user.groups.all()) | Q(page__in = request.user.pages.all())))[counter:][:10]
	context = {'posts':posts,}
	return render(request, 'home/home-page.html', context)

@login_required
def ProfileView(request, pk):
	user = User.objects.get(pk=pk)
	post = Post.objects.filter(author=user, group=None, page=None)[:20]
	if not request.user in user.blocked.all():
		context = {'user':user, 'posts': post}
		return render(request, 'special/profile.html', context)

	else:
		HttpResponseRedirect(reverse('blocked'))



@login_required
def AddFriendView(request, pk):
	user = get_object_or_404(User, pk=pk)
	if not request.user in user.blocked.all() and not request.user in user.waiting.all():
		user.waiting.add(request.user)
		notify_group_name = 'notify_%d'% user.pk
		async_to_sync(channel_layer.group_send)( notify_group_name, {'type': 'chat_message', 'request_pk': render_to_string('fragments/nav/FriendRequest.html', {'req': request.user}, request)})
	elif not request.user in user.blocked.all() and request.user in user.waiting.all():
		user.waiting.remove(request.user)
		notify_group_name = 'notify_%d'% user.pk
		async_to_sync(channel_layer.group_send)( notify_group_name, {'type': 'chat_message', 'request_delete': request.user.pk})
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def BlockUser(request, pk):
	user = get_object_or_404(User, pk=pk)
	if user in request.user.friends.all():
		request.user.friends.remove(user)
		user.friends.remove(request.user)
		request.user.blocked.add(user)

	elif request.user in user.waiting.all():
		user.waiting.remove(request.user)
		request.user.waiting_for.remove(user)
		request.user.blocked.add(user)

	else:
		request.user.blocked.add(user)

	try:
		crush = UserCrushs.objects.get((Q(user=request.user, crush=user)| Q(user=user, crush=request.user)))
		crush.delete()
	
	except:
		pass

	return HttpResponseRedirect(reverse('home'))


@login_required
def AcceptFriend(request, pk):
	user = get_object_or_404(User, pk=pk)
	user.waiting_for.remove(request.user)
	request.user.waiting.remove(user)
	user.friends.add(request.user)
	request.user.friends.add(user)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def DenyFriend(request, pk):
	user = get_object_or_404(User, pk=pk)
	user.waiting_for.remove(request.user)
	request.user.waiting.remove(user)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def CancelRequest(request, pk):
	user = get_object_or_404(User, pk=pk)
	user.waiting_for.remove(request.user)
	request.user.waiting.remove(user)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def RemoveFriendView(request, pk):
	user = get_object_or_404(User, pk=pk)
	user.waiting_for.remove(request.user)
	request.user.waiting.remove(user)

	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def FollowUser(request, pk):
	user = get_object_or_404(User, pk=pk)
	if user in request.user.following.all():
		request.user.following.remove(user)
	else:
		request.user.following.add(user)
	
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def CrushOnUser(request, pk):
	user = get_object_or_404(User, pk=pk)
	try:
		crush = UserCrushs.objects.get(user=request.user, crush=user)
		crush.delete()
	except:
		UserCrushs.objects.create(user=request.user, crush=user)

	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def SearchView(request):
	if request.method == 'POST':
		searched = request.POST.get('searched')
		search = Search.objects.create(searcher=request.user, searched=searched)

		posts = []
		pages = []
		groups = []
		users = []

		for word in searched.split():
			filtered_posts = Post.objects.filter(content__contains=word)
			filtered_groups = Group.objects.filter(group_name__contains=word)
			filtered_pages = Page.objects.filter(page_name__contains=word)
			filtered_users =  User.objects.filter(name__contains=word)
			
			for (user, post, page, group) in itertools.zip_longest(filtered_users, filtered_posts, filtered_pages, filtered_groups):
				users.append(user)
				posts.append(post)
				pages.append(page)
				groups.append(group)


		ordered_users = [item for items, c in Counter(users).most_common() for item in [items] * c]
		ordered_posts = [item for items, c in Counter(posts).most_common() for item in [items] * c]
		ordered_groups = [item for items, c in Counter(groups).most_common() for item in [items] * c]
		ordered_pages = [item for items, c in Counter(pages).most_common() for item in [items] * c]

		freq_users = Counter(users)
		freq_posts = Counter(posts)
		freq_groups = Counter(groups)
		freq_pages = Counter(pages)

		common_users = [ele for ele in users if freq_users[ele] > int(len(searched.split())-1)]
		common_posts = [ele for ele in posts if freq_posts[ele] > int(len(searched.split())-1)]
		common_groups = [ele for ele in groups if freq_groups[ele] > int(len(searched.split())-1)]
		common_pages = [ele for ele in pages if freq_pages[ele] > int(len(searched.split())-1)]
		

		cleaned_users = list(dict.fromkeys(users))
		cleaned_posts = list(dict.fromkeys(posts))
		cleaned_groups = list(dict.fromkeys(groups))
		cleaned_pages = list(dict.fromkeys(pages))


		
		print("posts:", cleaned_posts)
		print("groups:", cleaned_groups)
		print("pages:", cleaned_pages)
		print("users:", cleaned_users)
		return render(request, 'home/search.html', {'search':search, 'searched':searched, 'posts':cleaned_posts, 'users':cleaned_users, 'pages':cleaned_pages, 'groups':cleaned_groups, })


	else:
		return render(request, 'home/search.html',)



@login_required
def PageView(request, pk):
	page = get_object_or_404(Page, pk=pk)
	if not request.user in page.page_blocked_members.all():
		return render(request, 'special/page.html', {'page': page})
	else:
		return render(request, 'special/blocked.html')

@login_required
def GroupView(request, pk):
	group = get_object_or_404(Group, pk=pk)
	if not request.user in group.group_members_blocked.all():
		return render(request, 'special/group.html', {'group': group})
	else:
		return render(request, 'special/blocked.html')

@login_required
def GroupRequestsView(request, pk):
	group = get_object_or_404(Group, pk=pk)
	if request.method == 'POST':

		JoinRequest= group.group_members_waiting.filter(request.user).exsists()

		if JoinRequest:
			JoinRequest.delete()
			return JsonResponse({'removed': True})
		else:
			group.group_members_waiting.add(request.user)

			return JsonResponse({'done': True})
	else:
		if request.user == group.group_admin or request.user in group.group_sub_admin.all():
			return render(request,'special/group/group-requests.html', {'group': group})
		else:
			return HttpResponseRedirect((reverse('group', args=[str(group.pk),])))

@login_required
def GroupPostsPerm(request, pk):
	group = get_object_or_404(Group, pk=pk)
	if request.user in group.group_sub_admin.all() or request.user == group.group_admin:
		posts = group.post_group.filter(accepted=False)[:20]
		return render(request, 'special/group/group-posts-permission.html', {'posts': posts})
	else:
		return HttpResponseRedirect((reverse('group', args=[str(pk)])))

@login_required
def LeaveGroupView(request, pk):
	group = Group.objects.get(pk=pk)
	
	if request.user != group.group_admin:
		group.group_members.remove(request.user)
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	
	else:
		group.delete()
		return HttpResponseRedirect('home')
	
@login_required
def GroupFixedPosts(request, pk):
	group = get_object_or_404(Group, pk=pk)
	if request.user in group.group_members.all():
		posts = group.post_group.filter(fixed=True)[:10]
		return render(request, 'special/group/group-fixed-posts.html', {'group': group, 'posts': posts})

	else:
		return HttpResponseRedirect((reverse('group', args=[str(pk)])))

@login_required
def GroupMembersView(request, pk):
	group = get_object_or_404(Group, pk=pk)
	if request.is_ajax():
		return JsonResponse(render_to_string('special/group/group-members.html', {'group':group}, request), safe=False)
	return render(request, 'special/group/group-members.html', {'group':group})

@login_required
def ModifySearch(request, pk, _type, searchedPK):
	search = Search.objects.get(pk=pk)

	if _type == 1:
		search.user = User.objects.get(pk=searchedPK)
		search.save()

		return HttpResponseRedirect((reverse('profile', args=[str(searchedPK)])))

	elif _type == 2:
		search.page = Page.objects.get(pk=searchedPK)
		search.save()
		return HttpResponseRedirect((reverse('page', args=[str(searchedPK)])))

	elif _type == 3:
		search.group = Group.objects.get(pk=searchedPK)
		search.save()
		return HttpResponseRedirect((reverse('group', args=[str(searchedPK)])))

	else:
		pass

def Blocked(request):
	return render(request, 'special/blocked.html')

def GroupBlockingUser(group , user):
	if user in group.group_members.all():
		group.group_members.remove(user)
	elif user in group.group_sub_admin.all():
		group.group_sub_admin.remove(user)
	elif user in group.group_members_waiting.all():
		group.group_members_waiting.remove(user)
	group.group_members_blocked.remove(user)

	return JsonResponse({'done':True})


def GroupAssignUserToAdmin(group , user):
	group.group_admin = user
	group.save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def GroupAssignUserToSubAdmin(group , user):
	group.group_sub_admin.add(user)
	return JsonResponse({'done':True})

def GroupAssignToUser(group , user):
	if user in group.group_sub_admin.all():
		group.group_sub_admin.remove(user)
		return JsonResponse({'done':True})
	else:
		return JsonResponse({'done': False})

def GroupMembersAssigns(request):
	if request.method == 'POST' and request.user == group.group_admin:
		user = User.objects.get(pk=request.POST.get('UserPk'))
		group = Group.objects.get(pk=request.POST.get('GroupPk'))
		assign = request.POST.get('assign')
		if assign == 'admin':
			return GroupAssignUserToAdmin(group, user)
		elif assign == 'subadmin':
			return GroupAssignUserToSubAdmin(group, user)
		elif assign == 'user':
			return GroupAssignToUser(group, user)
		elif assign == 'block':
			return GroupBlockingUser(group, user)
	else :
		raise PermissionDenied()

def GroupRulesView(request, group_id):
	group = get_object_or_404(Group, pk=group_id)
	return render(request, 'group/rules.html', {'group': group})

def GroupMemberProfile(request, group_id, user_id):
	group = get_object_or_404(Group, pk=group_id)
	if request.user in group.group_members.all():
		user = User.objects.get(pk=user_id)
		posts = Post.objects.filter(group=group, author=user, accepted=True)[:10]
		return render(request, 'special/group/MemberProfile.html', {'group': group, 'user': user, 'posts': posts})
	else:
		return PermissionDenied()

def GetGroupMembers(request, pk):
	searched = request.GET.get('searched')
	group = Group.objects.get(pk=pk)
	members = group.group_members.filter(name__contains = searched.capitalize())[:20]
	rendered = []
	for m in members:
		rendered.append(render_to_string('fragments/group/member.html', {'member': m, 'group':group}, request))
	if not members:
		return JsonResponse({'Found': False})
	else:
		return JsonResponse(rendered, safe=False)
@login_required
def InviteMembers(request, pk):
	group = Group.objects.get(pk=pk)
	if request.user in group.group_members.all():
		if not request.method == 'POST':
			users = request.user.user_friends.all().exclude(group__in = groups)
			rendered = [render_to_string('fragments/group/inviting-members.html', {'user': user}, request) for user in users]
			return JsonResponse(rendered, safe=False)
		else:
			Notifications.objects.create(receiver=User.objects.get(pk=request.POST.get('user_pk')), sender=request.user, notifications_type=12, notifications_obj=5, group=group, text_preview = "{0} invited you to join his group {1}".format(request.user.full_name(), group.group_namee))
	else:
		return HttpResponseRedirect((reverse('group', args=[str(pk),])))	

def AcceptGroupJoinReq(request):
	if request.method == 'POST':
		group_pk = request.POST.get('group')
		group = Group.objects.filter(pk=group_pk)[0]
		if not group:
			return JsonResponse({'success': False})
		user_pk = request.POST.get('user')
		user = User.objects.filter(pk=user_pk)[0]
		if not user:
			return JsonResponse({'success': False})
		group.group_members.add(user)
		group.group_members_waiting.remove(user)
		return JsonResponse({'success': True})

def DenyGroupJoinReq(request):
	if request.method == 'POST':
		group_pk = request.POST.get('group')
		group = Group.objects.filter(pk=group_pk)[0]
		if not group:
			return JsonResponse({'success':False})
		user_pk = request.POST.get('user')
		user = User.objects.filter(pk=user_pk)[0]
		if not user:
			return JsonResponse({'success': False})
		group.group_members_waiting.remove(user)
		return JsonResponse({'success': True})
@login_required
def UserFriendsPage(request):
	return render(request, 'special/profile/friends.html')