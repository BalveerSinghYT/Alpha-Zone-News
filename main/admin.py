from django.contrib import admin

# Register your models here.
from .models import BlogModel

admin.site.register(BlogModel)