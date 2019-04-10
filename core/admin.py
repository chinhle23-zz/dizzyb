from django.contrib import admin
from .models import Task, Note

# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('description', 'owner', 'created_at', 'completed_at', 'show_on')

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('task', 'text', 'created_at')