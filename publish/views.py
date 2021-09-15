from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import *
from .forms import *
from .models import *
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.utils.decorators import method_decorator
from django.views.generic import *
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView
from django.forms import inlineformset_factory
from media.models import Notifications
from django.template.loader import render_to_string
from django.http import HttpResponseNotFound
# Create your views here.
@login_required
def PostDetail(request, pk):
	post = Post.objects.filter(pk=pk)
	if not post:
		raise HttpResponseNotFound()
	return render(request, 'unique/post.html', {'post': post[0]})
@login_required
def CreatePost(request):
	if request.POST:
		form = ExtendedPostForm(request.POST or None, request.FILES or None)
		if request.POST.get("content") or request.FILES.getlist("files"):
			files = request.FILES.getlist("files")

			post = Post.objects.create(author=request.user, content = request.POST.get("content" or None))
			index = 0

			print(len(files))
			for file in files:
				pre_caption = "img_caption_" + str(index)
				caption = request.POST.get(pre_caption)

				PostFiles.objects.create(post=post, media=file, caption=caption)
				
				
				print("created")
				index = index+1
			return JsonResponse({"success": True})
		else:
			return render(request, 'home/home-page.html', {'messages':"at least one input is required"})

	else:
		return HttpResponseRedirect(reverse('home'))


		
@login_required
def UpdatePost(request, pk):
	post = get_object_or_404(Post, pk=pk)

	if request.user == post.author:
		form = inlineformset_factory(Post, PostFiles, fields=('caption', 'media'))
		form = form(instance=post)
		return render(request, 'publish/update-post.html', {'form': form, 'post':post})



@login_required
def CreateComment(request, pk):
	if request.POST:
		try:
			post = Post.objects.get(pk=pk)
		except:
			return JsonResponse({'success':False})
		content = request.POST.get('content')
		media = request.FILES.get('media') if request.FILES.get('media') else None
		comment = Comment.objects.create(post=post, author=request.user, content=content, media=media)
		form = render_to_string('fragments/snippets/comment.html', {'comment': comment} , request)
		return JsonResponse({'comment': form,})
		return render(request, 'home/home-page.html')
@login_required
def CreateReply(request, pk):
	if request.POST:
		form = ReplyForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			comment = Comment.objects.get(pk=pk)
			form = form.save(commit=False)
			form.author = request.user
			form.comment = comment
			form.save()
			form = serializers.serialize('json', [form,])
			return JsonResponse({'reply': form,})
		else:
			return render(request, 'home/home-page.html')
@login_required
def CreateSnippet(request, pk):
	if request.POST:
		form = ReplyForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			reply = Reply.objects.get(pk=pk)
			form = form.save(commit=False)
			form.author = request.user
			form.reply = reply
			form.save()
			return JsonResponse({'reply': form,})
		else:
			return render(request, 'home/home-page.html')

@login_required
def SharingPost(request, pk):
	try:
		
		post = Post.objects.get(pk=pk)
		group_pk = request.POST.get('group_pk' or None)
		content = request.POST.get('caption' or None)
		if not group_pk is None:
			try:
				group = Group.objects.get(pk=group_pk)
				shared_post = Post.objects.create(author=request.user, share=post.share or post, content=content , group=group)
				shares = post.shared.all()
				if shares.count() == 1:
					counts = 1 + " Share"
				else:
					counts = shares.count() + " Shares"
				post.shared.add(request.user)
				if post.share:
					post.share.shared.add(request.user)
				return JsonResponse({'counts' : counts})
				
			except:
				return JsonResponse({"data": "Whops! something went wrong or the post has been deleted."})

		else:

			shared_post = Post.objects.create(author=request.user, content=content, share=post.share or post)
			shares = post.shared.all()
			if shares.count() == 1:
				counts = "1 Share"
			else:
				counts = "%d Shares"% shares.count()
			post.shared.add(request.user)
			if post.share:
					post.share.shared.add(request.user)
			return JsonResponse({'counts' : counts})
		
	except:
		return JsonResponse({"data": "Whops! something went wrong or the post has been deleted."})
	
	

def DeletePost(request, pk):
	if request.method == 'DELETE':
		try:
			post = Post.objects.get(pk=pk)
			post.delete()
			return JsonResponse({'done': True})
		except:
			return JsonResponse({'done': False})



@login_required
def GetPostComment(request, pk, counts):
	try:
		post = Post.objects.get(pk=pk)
		comments = Comment.objects.filter(post=post)[counts:][:10]
		rendered = []
		for comment in comments:
			serializer = render_to_string('fragments/snippets/comment.html', {'comment': comment})
			rendered.append(serializer)
		return JsonResponse(rendered, safe=False)

	except:
		return JsonResponse({'message':"Whops something went wrong or the objects has been deleted!"})


@login_required
def GetPosts(request, counts = 0):
	posts = Post.objects.filter()[counts:][:10]

	if not posts:
		return JsonResponse({'message':"No more content to display!"})

	else:
		data = []
		for post in posts:
			posst = render_to_string("special/post.html", {'post': post} , request)
			data.append(posst)
		return JsonResponse(data, safe=False)




def PostMiddleRender(request, post):
	return render_to_string('fragments/snippets/post/post-middle.html', {'post': post}, request)


def CreateReactNotify(request, _type , post, words):

	if request.user != post.author:
		existed_notify = post.likes.count() + post.love.count() + post.sad.count() + post.haha.count() + post.wow.count() + post.angry.count()
		if int(existed_notify) >= 1:
			for receiver in post.post_notify_people.all():
				Notifications.objects.create(post=post, receiver = receiver ,sender=request.user, notifications_type = _type, text_preview = "{0} and {1} {2} your post.".format(request.user.full_name(), existed_notify, words))
		else:
			for receiver in post.post_notify_people.all():
				Notifications.objects.create(post=post, receiver = post.author ,sender=request.user, notifications_type = _type, notifications_obj = 1 , text_preview = "{0} {1} your post.".format(request.user.full_name(), words))

	return print("done")


def RemovePostReact(request, pk):
	post = Post.objects.get(pk=pk)

	if request.user in post.likes.all():
		post.likes.remove(request.user)

	elif request.user in post.love.all():
		post.love.remove(request.user)

	elif request.user in post.haha.all():
		post.haha.remove(request.user)

	elif request.user in post.sad.all():
		post.sad.remove(request.user)

	elif request.user in post.wow.all():
		post.wow.remove(request.user)

	elif request.user in post.angry.all():
		post.angry.remove(request.user)

	else:
		pass

	post.save()

	return JsonResponse(PostMiddleRender(request, post), safe=False)

def postValidation(user, post):
	if post.page and user in post.page.page_blocked_members.all():
		return True
	elif post.group and user in post.group.group_members_blocked.all():
		return True
	elif user in post.author.blocked.all():
		return True
	elif post.author in user.blocked.all():
		return True
	else:
		return False

def LikePost(request, pk):
	post = Post.objects.get(pk=pk)
	if postValidation(request.user, post) == True:
		return JsonResponse({'blocked': True})

	elif request.user in post.likes.all():
		post.likes.remove(request.user)
		notify = Notifications.objects.filter(post=post, receiver=post.author, sender=request.user, notifications_type = 1)
		notify.delete()
		post.save()
		return JsonResponse(PostMiddleRender(request, post), safe=False)
	else:
		RemovePostReact(request, pk)
		post.likes.add(request.user)
		CreateReactNotify(request, 1, post, "liked")		
		return JsonResponse(PostMiddleRender(request, post), safe=False)
	


def LovePost(request, pk):
	post = Post.objects.get(pk=pk)
	if postValidation(request.user, post) == True:
		return JsonResponse({'blocked': True})
	elif request.user in post.love.all():
		post.love.remove(request.user)
		notify = Notifications.objects.filter(post=post, receiver=post.author, sender=request.user, notifications_type = 2)
		notify.delete()
		post.save()
		return JsonResponse(PostMiddleRender(request, post), safe=False)
	else:
		RemovePostReact(request, pk)
		post.love.add(request.user)
		CreateReactNotify(request, 2, post, "loved")
		return JsonResponse(PostMiddleRender(request, post), safe=False)
		


def SmilePost(request, pk):
	post = Post.objects.get(pk=pk)
	if postValidation(request.user, post) == True:
		return JsonResponse({'blocked': True})
	elif request.user in post.haha.all():
		post.haha.remove(request.user)
		notify = Notifications.objects.filter(post=post, receiver=post.author, sender=request.user, notifications_type = 3)
		notify.delete()
		post.save()
		print(post.reacts_count())
		return JsonResponse(PostMiddleRender(request, post), safe=False)
	else:
		RemovePostReact(request, pk)
		post.haha.add(request.user)
		CreateReactNotify(request, 3, post, "reacted haha on")
		return JsonResponse(PostMiddleRender(request, post), safe=False)
		




def SadPost(request, pk):
	post = Post.objects.get(pk=pk)
	if postValidation(request.user, post) == True:
		return JsonResponse({'blocked': True})
	elif request.user in post.sad.all():
		post.sad.remove(request.user)
		notify = Notifications.objects.filter(post=post, receiver=post.author, sender=request.user, notifications_type = 4)
		notify.delete()
		post.save()
		return JsonResponse(PostMiddleRender(request, post), safe=False)
	else:
		RemovePostReact(request, pk)
		post.sad.add(request.user)
		CreateReactNotify(request, 4, post, "reacted sad on")
		return JsonResponse(PostMiddleRender(request, post), safe=False)
		


def WowPost(request, pk):
	post = Post.objects.get(pk=pk)
	if postValidation(request.user, post) == True:
		return JsonResponse({'blocked': True})
	elif request.user in post.wow.all():
		post.wow.remove(request.user)
		notify = Notifications.objects.filter(post=post, receiver=post.author, sender=request.user, notifications_type = 5)
		notify.delete()
		post.save()
		return JsonResponse(PostMiddleRender(request, post), safe=False)
	else:
		RemovePostReact(request, pk)
		post.wow.add(request.user)
		CreateReactNotify(request, 5, post, "reacted wow on")
		return JsonResponse(PostMiddleRender(request, post), safe=False)
		


def AngryPost(request, pk):
	post = Post.objects.get(pk=pk)
	if postValidation(request.user, post) == True:
		return JsonResponse({'blocked': True})
	elif request.user in post.angry.all():
		post.angry.remove(request.user)
		notify = Notifications.objects.filter(post=post, receiver=post.author, sender=request.user, notifications_type = 6)
		notify.delete()
		post.save()
		return JsonResponse(PostMiddleRender(request, post), safe=False)
	else:
		RemovePostReact(request, pk)
		post.angry.add(request.user)
		CreateReactNotify(request, 6, post, "reacted angry on")
		return JsonResponse(PostMiddleRender(request, post), safe=False)
		


def SavePost(request):
	if request.method == 'POST':
		pk = request.POST.get('pk')
		try:
			post = Post.objects.get(pk=pk)
			if post in request.user.saved_posts.all():
				request.user.saved_posts.remove(post)
			else:
				request.user.saved_posts.add(post)

			return JsonResponse({"done": "done"})
		except:
			return JsonResponse({"error": "Whops something went wrong, or the object has been deleted."})
	else:
		return render(request, 'publish/SavedPosts.html')

def ActivatePostNotify(request, pk):
	try:
		post = Post.objects.get(pk=pk)
		if request.user in post.post_notify_people.all():
			post.post_notify_people.remove(request.user)
		else:
			post.post_notify_people.add(request.user)
		return JsonResponse({"done": "done"})
	except:
		return JsonResponse({"error": "Whops something went wrong, or the object has been deleted."})