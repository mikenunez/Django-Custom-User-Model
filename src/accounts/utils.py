
def image_profile_upload(instance, filename):
	username = instance.user.username
	userid = instance.user.pk
	basename, file_extension = filename.split(".")
	new_filename = '{}-{}.{}'.format(username, userid, file_extension)
	return 'accounts/{}/{}'.format(username, new_filename)