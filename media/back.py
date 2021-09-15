from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse
from .forms import SignUpForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.core import serializers
from .models import User

def AuthenticationView(request):
	if not request.user.is_authenticated:
		RegisterationForm = SignUpForm()
		log_cookies = request.COOKIES.get('users')
		users = []
		
		forms = {'signup': RegisterationForm, 'users': users}
		if request.POST:
			if 'signup' in request.POST:
				form = SignUpForm(request.POST)
				if form.is_valid():
					form.save()
					user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password1'],)
					login(request,user)
					respone = HttpResponseRedirect((reverse('home')))
					if log_cookies is None:
						respone.set_cookie('users', form.cleaned_data['email'], max_age = 86400)
						print("7 days")
						return respone
					else:
						if not request.POST['email'] in log_cookies:
							new_user = form.cleaned_data['email']
							log_cookies = log_cookies + str(new_user)
							respone.set_cookie('users', log_cookies, max_age = 86400)
					return respone
				else:
					forms['signup'] = form
					return render(request, 'auth/join.html', forms)
			else:
				email = request.POST['log_email']
				password = request.POST['log_password']
				try:
					user = User.objects.get(email=email)
					auth = authenticate(email=email, password=password)
					login(request, auth)
					print("authenticated")
					respone = JsonResponse({'auth': True})		
					if log_cookies is None:
						respone.set_cookie('users', email, max_age = 86400)
						print("7 days")
						return respone
					else:
						print("cookies not none")
						if not email in log_cookies:
							new_user = email
							log_cookies = log_cookies + str(" %s"% new_user)
							respone.set_cookie('users', log_cookies, max_age = 86400)
					return respone
				except:
					return JsonResponse({'auth': False})
		else:
			if not log_cookies is None:
				for email in log_cookies.split():
					user = User.objects.get(email=email)
					users.append(user)
				forms = {'signup': RegisterationForm, 'users': users}	
			return render(request, 'auth/join.html', forms)
			
	else:
		return HttpResponseRedirect((reverse('home')))