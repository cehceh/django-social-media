from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django.core.exceptions import ValidationError

class SignUpForm(UserCreationForm):
	first_name = forms.CharField(label='First name', max_length=100)
	last_name = forms.CharField(label='last name', max_length=100)
	email = forms.CharField(max_length=255, required=True, widget=forms.EmailInput())
	password1 = forms.CharField(label='Password', required=True, widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirm password', required=True, widget=forms.PasswordInput)
	birthday = forms.DateField(label='BirthDay', required=True, widget=forms.DateInput(attrs={'type': 'date'}))


	class Meta:
		model=User
		fields = ('first_name', 'last_name', 'email', 'password1', 'password2', 'gender', )

	def save(self):
		self.instance.name = str(self.cleaned_data['first_name'].capitalize() + " " + self.cleaned_data['last_name'])
		return super().save()

class GroupForm(forms.ModelForm):
	group_name = forms.CharField(label='Group name', max_length=200, required=True)
	group_cover_photo = forms.FileField(label='Group cover', required=True)
	class Meta:
		model = Group
		fields = ('group_name', 'group_cover_photo')

	def clean(self):
		if not self.cleaned_data['group_name'] and not self.cleaned_data['group_cover_photo']:
			raise ValidationError("both fields are required")