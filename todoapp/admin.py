from django.contrib import admin

from .models import TodoCategory, Todo


admin.site.register(TodoCategory)

admin.site.register(Todo)
# Register your models here.
