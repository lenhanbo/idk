from django.contrib import admin
from .models import user, Comment
# Register your models here.
admin.site.register(user)
admin.site.register(Comment)
