from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .models import *
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.template.loader import render_to_string
channel_layer = get_channel_layer()

@receiver(post_save, sender=UserCrushs)
def check_user_crush(sender, instance, created, **kwargs):
  crush = instance.crush
  user  = instance.user
  try:
    if_crush = UserCrushs.objects.get(user=crush, crush=user)
  except:
    if_crush = None

  if not if_crush is None:
    _notify = Notifications.objects.create(notifications_type=11, sender=crush, receiver=user, text_preview = 'Congratz love birds! you and {0} have a crush on each other.'.format(crush.full_name()))


    __notify = Notifications.objects.create(notifications_type=11, sender=user, receiver=crush, text_preview = 'Congratz love birds! you and {0} have a crush on each other.'.format(user.full_name()))
    



@receiver(post_save, sender=Notifications)
def AfterNotifies(sender, instance, **kwargs):
    notify_group_name = 'notify_%d'% instance.receiver.pk
    async_to_sync(channel_layer.group_send)(
        notify_group_name,
        {'type': 'chat_message', 'notify': render_to_string('fragments/nav/notify.html', {'notify': instance, 'request.user': instance.receiver})})


@receiver(post_delete, sender=Notifications)
def AfterNotifiesDelete(sender, instance, **kwargs):
    notify_group_name = 'notify_%d'% instance.receiver.pk
    async_to_sync(channel_layer.group_send)(
        notify_group_name,
        {'type': 'chat_message', 'notify_delete': instance.pk})


@receiver(post_save, sender=Group)
def AfterGroup(sender, instance, **kwargs):
    instance.group_members.add(instance.group_admin)
    instance.group_admin.groups.add(instance)

@receiver(post_save, sender=Page)
def AfterPage(sender, instance, **kwargs):
    instance.page_admin.pages.add(instance)