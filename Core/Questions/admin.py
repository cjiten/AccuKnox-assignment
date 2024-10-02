from django.contrib import admin

from .models import MyBlog, MyBlogtwo, MyBlogthree

# Register your models here.

admin.site.register(MyBlog),
admin.site.register(MyBlogtwo),
admin.site.register(MyBlogthree),