from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Tweet)
admin.site.register(Hashtag)
admin.site.register(Comment)
admin.site.register(User)
