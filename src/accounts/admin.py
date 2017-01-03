from django.contrib import admin

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from .models import MyUser
from .forms import UserChangeForm, UserCreationForm



class UserAdmin(BaseUserAdmin):
	# The forms to add and change user instances
	form = UserChangeForm
	add_form = UserCreationForm

	# The fields to be used in displaying the User model.
	# These override the definitions on the base UserAdmin
	# that reference specific fields on auth.User.
	list_display = ('username', 'is_admin', 'last_login',)
	list_filter = ('is_admin',)
	fieldsets = (
		(None, {'fields': ('username', 'password')}),
		# ('Personal info', {'fields': ('email',)}),
		('Permissions', {'fields': ('is_admin','user_permissions', 'groups')}),
	)
	# add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
	# overrides get_fieldsets to use this attribute when creating a user.
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('username', 'password1', 'password2')}
		),
	)
	search_fields = ('username',)
	ordering = ('username',)
	filter_horizontal = ('groups', 'user_permissions',)

# Now register the new UserAdmin...
admin.site.register(MyUser, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
# admin.site.unregister(Group)
