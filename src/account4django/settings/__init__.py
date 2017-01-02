from .base_settings import *

try:
	from .prod_settings import *
except:
	pass

try:
	from .local_settings import *
except:
	pass