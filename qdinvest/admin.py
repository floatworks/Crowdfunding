from django.contrib import admin
from models import *

# Register your models here.

class USERSAdmin(admin.ModelAdmin):
	list_display = ['u_name','u_pwd','u_tel','u_status']
	search_fiedls = ['u_name']

admin.site.register(USERS,USERSAdmin)

