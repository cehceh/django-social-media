from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from .forms import *
from .models import *
from media.models import User
from django.db.models import Q
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

channel_layer = get_channel_layer()

# Create your views here.

##Normal chat views
def Streaming(request):
	return render(request, 'streaming.html')

def SendMessageView(request):
	if request.method == "POST":
		partner = get_object_or_404(User, pk=request.POST.get('pk'))
		form = MessageForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			
			if request.POST.get('content'):
				text = request.POST.get('content')
				message = Message.objects.create(sender=request.user, receiver=partner, content = text)
			else:
				f = request.FILES.get('record')
				message = Message.objects.create(sender=request.user, receiver=partner, record = f)
			if request.FILES.getlist('file') != None:
				for file in request.FILES.getlist('file'):
					MessageMedia.objects.create(message = message, media=file)
			

			sender_m = render_to_string("fragments/room/Message.html", {'message': message} , request)
			message_group_name1 = 'chat_%d' % int(request.user.pk + partner.pk)
			async_to_sync(channel_layer.group_send)(
				message_group_name1,
				{'type': 'chat_message', 'message': sender_m})
			
		
			return JsonResponse({'done': True})
		else:
			return JsonResponse({'done': False})		

@login_required
def MessageView(request, partner_id):
	partner = get_object_or_404(User, pk=partner_id)
	messages 	= Message.objects.filter((Q(sender=request.user, receiver=partner)| Q(receiver = request.user, sender=partner))).order_by('date')
	sideMessages = [Message.objects.filter((Q(sender=request.user, receiver=user)| Q(receiver = request.user, sender=user))).last() for user in request.user.chatted_with.all()]
	form 		= MessageForm()
	context 	= {'messages': messages, 'form':form, 'partner':partner}

	if sideMessages:
		for m in sideMessages:
			if not m:
				sideMessages.remove(m)
		context['side_messages'] = sideMessages

	return render(request, 'chat/messages/room.html', context)
	

def DeleteMessage(request):
	pk = request.DELETE.get('id')
	message = Message.objects.filter(pk=pk)[0]
	if not message:
		return JsonResponse({'done': False})
	if request.method == 'DELETE' and request.user == message.sender:
		message.delete()

		return JsonResponse({'done': True})
	
	else:
		raise PermissionDenied()

##Secret Rooms Views
@login_required
def AnonymousChatView(request, pk):
	user = User.objects.get(pk=pk)

	if user.allow_anonymous == False:
		raise PermissionDenied()

	elif not request.user in user.blocked.all() and not user in request.user.blocked.all():
		room = AnonymousRoom.objects.filter(creator = request.user, partner = user)
		return render(request, 'chat/anonymous-messages/room.html', {'room': room})

	else:
		raise PermissionDenied()