from django import forms
from .models import *
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):
	content = forms.CharField(max_length=100, required=False)
	class Meta:
		model= Post
		fields = ('content',)

class ExtendedPostForm(PostForm):
	Files = forms.FileField(required=False, widget=forms.FileInput(attrs={'multiple': 'true',
		'onchange': "ReveiwPost(this);"}))


	class Meta(PostForm.Meta):
		fields = PostForm.Meta.fields + ('Files',)

	def clean(self):
		if not self.cleaned_data['content'] and not self.cleaned_data['Files'] :
			raise ValidationError("at least one field is required")

class CommentForm(forms.ModelForm):
	content = forms.CharField(max_length=255, required=True)
	img = forms.ImageField(required=False)

	class Meta:
		model= Comment
		fields = ('content', 'img',)
