from django.contrib import admin

from .models import Room, Message

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('creator', 'name', 'created')
    search_fields = ('name',)
    ordering = ('-created',)
    list_filter = ('public',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('author', 'created')
