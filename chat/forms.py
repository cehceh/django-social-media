from django import forms
from .models import *
from django.core.exceptions import ValidationError

class MessageForm(forms.ModelForm):
	content = forms.CharField(required=False ,max_length=255)
	file = forms.FileField(required=False, widget=forms.FileInput(attrs={'multiple': 'true'}))
	record = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'hidden'}))
	class Meta:
		model=Message
		fields = ('content', 'record', 'file')

	def clean(self):
		if not self.cleaned_data['content'] and not self.cleaned_data['record']:
			raise ValidationError("You must specify either content or record")
