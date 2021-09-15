from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()

videosEx = ('webm', 'mp4', 'mkv')
@register.filter(is_safe = True)
@stringfilter
def videoEx(name):
    if name.lower().endswith(videosEx):
        return True
    else:
        return False

@register.filter(is_safe=True)
@stringfilter
def mediaEx(arg):
    if videoEx(arg) == True:
        return mark_safe("<video src='" + arg + "'style='width:150px; height:150px'></video>")
    else:
        return mark_safe("<img src='" + arg + "'style='width:150px; height:150px'>")