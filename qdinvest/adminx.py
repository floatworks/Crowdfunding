import xadmin
from xadmin import views
from models import *

# Register your models here.

class USERSAdmin(object):
	list_display = ['u_name','u_pwd','u_tel','u_status']
	search_fiedls = ['u_name']

xadmin.site.register(USERS,USERSAdmin)

