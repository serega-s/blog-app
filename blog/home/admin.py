from django.contrib import admin

from .models import *

admin.site.register(BlogModel)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Like)
