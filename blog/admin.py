from django.contrib import admin
import os
from blog.models import *

# Register your models here.

admin.sites.AdminSite.site_title = "پنل"
admin.sites.AdminSite.site_header = "پنل مدیریت جنگو"
admin.sites.AdminSite.index_title = "مدیریت"

# Inlines
class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = ["author", "title", "description", "slug", "publish", "status", "reading_time"]
    list_display = ["title", "author", "publish", "status"]
    list_filter = ["publish", "status"]
    search_fields = ["title", "description"]
    list_editable = ["publish", "status"]
    inlines = [
        ImageInline,
        CommentInline
    ]

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    fields = ["name", "subject", "message", "email", "phone"]
    list_display = ["name", "subject", "message", "email", "phone"]
    list_filter = ["name"]
    search_fields = ["name", "subject", "message"]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', "name", "created", "active"]
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'body']
    list_editable = ['active']

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['post', "title", "created"]
