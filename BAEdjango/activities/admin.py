from django.contrib import admin

# Register your models here.
from .models import Catlist, Mainbae
admin.site.register(Catlist)
admin.site.register(Mainbae)
