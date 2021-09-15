from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def is_img(name):
	if name.lower().endswith(('png', 'jpg', 'jpeg')):
		return True
	else:
		return False


