from publish.forms import *
from media.models import *
from chat.models import *

def Forms(request):
	if request.user.is_authenticated:
		post_form = ExtendedPostForm()
		comment_form = CommentForm()
		notifies = Notifications.objects.filter(receiver = request.user)
		searchs = Search.objects.filter(searcher=request.user)
		messages = [Message.objects.filter((Q(sender=request.user, receiver=user)| Q(receiver = request.user, sender=user))).last() for user in request.user.chatted_with.all()]
		for m in messages:
			if not m:
				messages.remove(m)
		return {
		'post_form': post_form,
		'comment_form': comment_form,
		'notifies': notifies,
		'searchs': searchs,
		'navmessages': messages if messages else None
		}
	else:
		return {
		'message': "sb7",
		}