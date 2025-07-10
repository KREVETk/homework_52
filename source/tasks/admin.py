from django.contrib import admin

from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('description', 'status', 'due_date')
    list_filter = ('status',)
    search_fields = ('description',)
