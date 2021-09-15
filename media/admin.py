from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import *
# Register your models here.


class ManagingUsers(UserAdmin):

	add_form = SignUpForm

	list_display = ['email']
	search_fields = ['email']
	readonly_fields = ['date_joined', 'last_login']
	ordering = ('email',)

	filter_horizontal = []
	list_filter = []


	add_fieldsets = (

		('Add a new user', {
			'classes':('wide',),
			'fields': ('name','email', 'birthday', 'password1', 'password2', 'pic', 'cover', 'validated', 'is_admin', 'is_staff', 'is_active', 'is_superuser'),
			}),
		)
	
	fieldsets = (

		(None, {
			'fields': ('name',  'chatted_with' , 'bio', 'email', 'BirthDate', 'password', 'pic', 'cover', 'is_admin', 'is_staff', 'is_active', 'is_online', 'is_superuser', 'date_joined', 'friends', 'blocked', 'waiting', 'following', 'followers', 'pages', 'groups', 'validated')
			}),

		)
admin.site.register(User, ManagingUsers)
admin.site.register(Group)
admin.site.register(Country)
admin.site.register(Government)
admin.site.register(Page)
admin.site.register(Notifications)
admin.site.register(UserCrushs)
admin.site.register(Search)

