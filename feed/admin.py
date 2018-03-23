from django.contrib import admin

from .models import Action, Post, Comment

@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('verb', 'created')
    search_fields = ('verb',)
    ordering = ('-created',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('text', 'image')
    search_fields = ('text',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('action', 'user', 'created')
