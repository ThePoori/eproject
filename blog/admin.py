from django.contrib import admin

from blog.models import Post, Ticket

# Register your models here.

admin.sites.AdminSite.site_title = "پنل"
admin.sites.AdminSite.site_header = "پنل مدیریت جنگو"
admin.sites.AdminSite.index_title = "مدیریت"

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = ["author", "title", "description", "slug", "publish", "status"]
    list_display = ["title", "author", "publish", "status"]
    list_filter = ["publish", "status"]
    search_fields = ["title", "description"]
    list_editable = ["publish", "status"]

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    fields = ["name", "subject", "message", "email", "phone"]
    list_display = ["name", "subject", "message", "email", "phone"]
    list_filter = ["name"]
    search_fields = ["name", "subject", "message"]
