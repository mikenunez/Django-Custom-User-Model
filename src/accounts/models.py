from django.db import models

from django.db.models.signals import post_save
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.core.validators import RegexValidator
from django.contrib.auth.models import (
	BaseUserManager, AbstractBaseUser, PermissionsMixin
)

from .utils import image_profile_upload


USERNAME_REGEX = '^[a-zA-Z0-9.-]*$'


class MyUserManager(BaseUserManager):

	def create_user(self, username, email, password=None):
		"""
		Creates and saves a User with the given email, date of
		birth and password.
		"""
		if not email:
			raise ValueError('Users must have an email address')

		user = self.model(
			username=username,
			email=self.normalize_email(email),
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, username, email, password):
		"""
		Creates and saves a superuser with the given email, date of
		birth and password.
		"""
		user = self.create_user(
			username,
			email,
			password=password,
		)
		user.is_admin = True
		user.save(using=self._db)
		return user



@python_2_unicode_compatible
class MyUser(AbstractBaseUser,PermissionsMixin):
	username = models.CharField(
		max_length=100,
		unique=True,
		validators=[
			RegexValidator(
				regex = USERNAME_REGEX,
				message = 'Username must be Alpahnumeric or contain ".", "-"',
				code='invalid_username'
			)],
	)
	# profile = models.OneToOneField(Profile)
	# email = models.EmailField(
	# 	verbose_name='email address',
	# 	max_length=255,
	# 	unique=True,
	# )
	date_joined = models.DateTimeField(auto_now_add=True)

	is_paid = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=True)
	is_active = models.BooleanField(default=True)

	objects = MyUserManager()

	USERNAME_FIELD = 'username'
	# REQUIRED_FIELDS = ['email']

	def __str__(self):
		return self.email

	def get_full_name(self):
		# The user is identified by their email address
		return self.username

	def get_short_name(self):
		# The user is identified by their email address
		return self.email

	def has_perm(self, perm, obj=None):
		"Does the user have a specific permission?"
		# Simplest possible answer: Yes, always
		return True

	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?"
		# Simplest possible answer: Yes, always
		return True



@python_2_unicode_compatible
class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	email = models.EmailField(
		verbose_name='email address',
		max_length=255,
		unique=True,
	)
	firstname	= models.CharField(max_length= 100, null=True, blank=True)
	lastname	= models.CharField(max_length= 100, null=True, blank=True)
	phone		= models.CharField(max_length= 30, null=True, blank=True)
	facebook	= models.CharField(max_length= 100, null=True, blank=True)
	twitter		= models.CharField(max_length= 100, null=True, blank=True)
	instagram	= models.CharField(max_length= 100, null=True, blank=True)
	linkedin	= models.CharField(max_length= 100, null=True, blank=True)
	image 		= models.ImageField(upload_to=image_profile_upload)
	# PYTZ
	import pytz
	timezone = forms.ChoiceField(
        verbose_name='time zone',
        choices=[(t, t) for t in pytz.common_timezones]
    )

	
	def __str__(self):
		return str(self.user.username)

def create_user_profile(sender, instance, created, *args, **kwargs):
    if created:
        try:
            Profile.objects.create(user=instance)
            # ActivationProfile.objects.create(user=instance)
        except:
            pass

post_save.connect(create_user_profile, sender=settings.AUTH_USER_MODEL)