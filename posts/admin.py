from django.contrib import admin
from .models import Post, LikeDislike

# Register your models here.

admin.site.register(Post)
admin.site.register(LikeDislike)